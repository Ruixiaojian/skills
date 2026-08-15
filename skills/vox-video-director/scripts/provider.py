#!/usr/bin/env python3
"""Media-provider abstraction used by every Vox Video Director pipeline stage.

The default backend is ``bailian_cli``.  It shells out to the authenticated
``bl`` executable instead of handling DashScope credentials or HTTP requests
inside this project.  Atlas Cloud remains available as ``atlas_cloud`` for
backwards compatibility.

The stage scripts use an asynchronous submit/poll API.  ``bl`` image, video and
speech commands normally wait and save a local file, so BailianCliProvider starts
each CLI command in a child process and exposes that process as a lightweight job.
This preserves the pipeline's existing parallelism without leaking API keys.
"""
import glob
import json
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from abc import ABC, abstractmethod

import atlas_cloud


class ProviderError(RuntimeError):
    pass


class Provider(ABC):
    name = "base"
    supports_music = True
    supports_stall_resubmit = True
    max_parallel = None

    @abstractmethod
    def submit_image(self, model, prompt, **params): ...
    @abstractmethod
    def submit_video(self, model, prompt, **params): ...
    @abstractmethod
    def submit_audio(self, model, **params): ...
    @abstractmethod
    def remove_bg(self, model, image_url, **params): ...
    @abstractmethod
    def get_status(self, job_id): ...
    @abstractmethod
    def upload(self, path): ...
    @abstractmethod
    def download(self, url, dest): ...
    @abstractmethod
    def transcribe(self, audio, **params): ...


class BailianCliProvider(Provider):
    """Adapter for Aliyun Model Studio's ``bl`` CLI.

    Local inputs are passed straight to ``bl``; the CLI uploads them to temporary
    DashScope storage when required.  Outputs are always downloaded into a private
    temporary directory first and then copied to the pipeline's requested path.
    """

    name = "bailian_cli"
    supports_music = False  # bl 1.14.x has image/video/TTS/ASR, but no music command.
    supports_stall_resubmit = False  # avoid duplicate billable CLI tasks
    max_parallel = 2  # conservative default for common DashScope account rate limits

    IMAGE_MODEL = "qwen-image-3.0"
    IMAGE_EDIT_MODEL = "qwen-image-3.0"
    VIDEO_MODEL = "happyhorse-1.1-i2v"
    VIDEO_EDIT_MODEL = "happyhorse-1.0-video-edit"
    VOICE_MODEL = "cosyvoice-v3-flash"
    DEFAULT_VOICE = "longtian_v3"

    def __init__(self):
        if not shutil.which("bl"):
            raise ProviderError(
                "bl is not installed. Install with: npm install -g bailian-cli"
            )
        self._root = tempfile.mkdtemp(prefix="vox-video-director-bl-")
        self._jobs = {}

    @staticmethod
    def _model(model, default):
        # Atlas model IDs contain a provider slash.  Mapping them lets older
        # beats.json files switch by changing only `provider`.
        return default if not model or "/" in model else model

    @staticmethod
    def _local(value):
        if not isinstance(value, str) or value.startswith(("http://", "https://", "oss://")):
            return value
        return os.path.abspath(value)

    def _start(self, kind, command, *, output=None, output_glob=None):
        job_id = f"bl-{kind}-{uuid.uuid4().hex[:12]}"
        log_path = os.path.join(self._root, f"{job_id}.log")
        log = open(log_path, "w", encoding="utf-8")
        try:
            process = subprocess.Popen(
                command, stdout=log, stderr=subprocess.STDOUT, text=True
            )
        except Exception:
            log.close()
            raise
        self._jobs[job_id] = {
            "process": process,
            "log": log,
            "log_path": log_path,
            "output": output,
            "output_glob": output_glob,
        }
        return job_id

    def submit_image(self, model, prompt, **params):
        images = params.pop("images", None) or []
        out_dir = os.path.join(self._root, uuid.uuid4().hex)
        os.makedirs(out_dir, exist_ok=True)
        prefix = "edited" if images else "image"
        if images:
            command = ["bl", "image", "edit"]
            for image in images:
                command += ["--image", self._local(image)]
            model = self._model(model, self.IMAGE_EDIT_MODEL)
        else:
            command = ["bl", "image", "generate"]
            model = self._model(model, self.IMAGE_MODEL)
        command += [
            "--prompt", prompt,
            "--model", model,
            "--out-dir", out_dir,
            "--out-prefix", prefix,
            "--watermark", "false",
            "--quiet",
        ]
        size = params.get("aspect_ratio") or params.get("size")
        if size:
            command += ["--size", str(size).replace("x", "*")]
        if params.get("seed") is not None:
            command += ["--seed", str(params["seed"])]
        return self._start(
            "image", command, output_glob=os.path.join(out_dir, f"{prefix}*")
        )

    def submit_video(self, model, prompt, **params):
        out = os.path.join(self._root, f"video-{uuid.uuid4().hex}.mp4")
        source_video = params.get("video")
        refs = params.get("reference_videos") or []
        if source_video or refs:
            source_video = source_video or refs[0]
            model = self._model(model, self.VIDEO_EDIT_MODEL)
            command = [
                "bl", "video", "edit",
                "--video", self._local(source_video),
                "--prompt", prompt,
            ]
        else:
            model = self._model(model, self.VIDEO_MODEL)
            command = ["bl", "video", "generate", "--prompt", prompt]
            if params.get("image"):
                command += ["--image", self._local(params["image"])]
        command += ["--model", model]
        duration = params.get("duration")
        if duration is not None:
            # Happyhorse currently validates 3s minimum server-side, even though
            # older CLI help text listed 2s. Assembly trims it to the requested shot.
            command += ["--duration", str(max(3, min(10, int(round(float(duration))))))]
        ratio = params.get("ratio") or params.get("aspect_ratio")
        if ratio:
            command += ["--ratio", str(ratio)]
        resolution = params.get("resolution")
        if resolution:
            command += ["--resolution", str(resolution).upper()]
        command += ["--watermark", "false", "--download", out, "--quiet"]
        return self._start("video", command, output=out)

    def submit_audio(self, model, **params):
        if "music" in (model or "").lower() or "prompt" in params and "text" not in params:
            raise ProviderError(
                "bl 1.14.x does not expose music generation. Set bgm_path in beats.json "
                "to an existing instrumental audio file, or run without BGM."
            )
        if params.get("references"):
            raise ProviderError(
                "Local reference-audio voice cloning is not exposed by bl speech synthesize. "
                "Use a pre-created CosyVoice voice ID in voice.voice_id."
            )
        out = os.path.join(self._root, f"speech-{uuid.uuid4().hex}.mp3")
        model = self._model(model, self.VOICE_MODEL)
        voice = params.get("voice") or params.get("voice_id") or self.DEFAULT_VOICE
        # Atlas defaults are not valid CosyVoice IDs; preserve old project files.
        if voice in {"leo", "rex", "sal", "ara", "eve"} or len(str(voice)) == 12:
            voice = self.DEFAULT_VOICE
        command = [
            "bl", "speech", "synthesize",
            "--text", str(params.get("text", "")),
            "--model", model,
            "--voice", str(voice),
            "--format", "mp3",
            "--out", out,
            "--quiet",
        ]
        if params.get("language"):
            command += ["--language", str(params["language"])]
        rate = params.get("rate", params.get("speed"))
        if rate is not None:
            command += ["--rate", str(rate)]
        if params.get("instruction"):
            command += ["--instruction", str(params["instruction"])]
        return self._start("speech", command, output=out)

    def remove_bg(self, model, image_url, **params):
        return self.submit_image(
            self.IMAGE_EDIT_MODEL,
            "Remove the background and keep only the foreground subject on a clean transparent background.",
            images=[image_url],
        )

    def get_status(self, job_id):
        job = self._jobs.get(job_id)
        if not job:
            return {"status": "failed", "output": None, "error": f"unknown job {job_id}"}
        code = job["process"].poll()
        if code is None:
            return {"status": "pending", "output": None, "error": None}
        if not job["log"].closed:
            job["log"].close()
        with open(job["log_path"], encoding="utf-8", errors="replace") as f:
            log = f.read()
        if code != 0:
            return {"status": "failed", "output": None, "error": log[-1200:]}
        output = job.get("output")
        if not output and job.get("output_glob"):
            matches = [p for p in glob.glob(job["output_glob"]) if os.path.isfile(p)]
            output = matches[0] if matches else None
        if not output or not os.path.exists(output) or os.path.getsize(output) == 0:
            return {
                "status": "failed", "output": None,
                "error": f"bl completed but no output file was found. Log: {log[-800:]}",
            }
        return {"status": "completed", "output": output, "error": None}

    def upload(self, path):
        # bl accepts local paths and performs the temporary upload itself.
        return self._local(path)

    def download(self, url, dest):
        os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            subprocess.run(["/usr/bin/curl", "-fsSL", "--retry", "3", "-o", dest, url], check=True)
        else:
            src = os.path.abspath(url)
            if src != os.path.abspath(dest):
                shutil.copy2(src, dest)
        if not os.path.exists(dest) or os.path.getsize(dest) == 0:
            raise ProviderError(f"download produced an empty file: {url}")
        return dest

    def transcribe(self, audio, **params):
        out = os.path.join(self._root, f"asr-{uuid.uuid4().hex}.json")
        command = [
            "bl", "speech", "recognize", "--url", self._local(audio),
            "--model", str(params.get("model", "fun-asr")), "--out", out,
            "--quiet",
        ]
        if params.get("language"):
            command += ["--language", str(params["language"])]
        run = subprocess.run(command, capture_output=True, text=True)
        if run.returncode != 0:
            raise ProviderError(f"bl speech recognize failed: {(run.stderr or run.stdout)[-1200:]}")
        with open(out, encoding="utf-8") as f:
            raw = json.load(f)
        return _normalize_bailian_asr(raw, params.get("language"))


def _normalize_bailian_asr(raw, language=None):
    """Normalize FunASR's downloaded transcription JSON to Vox Video Director's schema."""
    transcripts = raw.get("transcripts", []) if isinstance(raw, dict) else []
    words, texts, duration_ms = [], [], 0
    for transcript in transcripts:
        if transcript.get("text"):
            texts.append(transcript["text"])
        duration_ms = max(duration_ms, int(transcript.get("content_duration_in_milliseconds", 0) or 0))
        for sentence in transcript.get("sentences", []) or []:
            sentence_words = sentence.get("words", []) or []
            if sentence_words:
                for word in sentence_words:
                    start = float(word.get("begin_time", word.get("start_time", 0)) or 0) / 1000
                    end = float(word.get("end_time", word.get("end", 0)) or 0) / 1000
                    text = str(word.get("text", "")) + str(word.get("punctuation", ""))
                    words.append({"text": text, "start": start, "end": end})
                    duration_ms = max(duration_ms, int(end * 1000))
            else:
                start = float(sentence.get("begin_time", 0) or 0) / 1000
                end = float(sentence.get("end_time", 0) or 0) / 1000
                words.append({"text": sentence.get("text", ""), "start": start, "end": end})
                duration_ms = max(duration_ms, int(end * 1000))
    text = " ".join(texts).strip() or " ".join(w["text"] for w in words).strip()
    return {"text": text, "language": language, "duration": duration_ms / 1000, "words": words}


class AtlasCloudProvider(Provider):
    name = "atlas_cloud"

    def submit_image(self, model, prompt, **params):
        return atlas_cloud.submit_image(model, prompt, **params)

    def submit_video(self, model, prompt, **params):
        return atlas_cloud.submit_video(model, prompt, **params)

    def submit_audio(self, model, **params):
        return atlas_cloud.submit_media(model, **params)

    def remove_bg(self, model, image_url, **params):
        body = {"model": model, "image": image_url, **params}
        return atlas_cloud._post("/model/generateImage", body)["data"]["id"]

    def get_status(self, job_id):
        try:
            d = atlas_cloud._get(f"/model/prediction/{job_id}").get("data", {})
        except atlas_cloud.AtlasCloudError as e:
            return {"status": "failed", "output": None, "error": str(e)}
        st = d.get("status")
        if st in ("completed", "succeeded"):
            out = d.get("outputs") or d.get("output")
            out = out[0] if isinstance(out, list) else out
            return {"status": "completed", "output": out, "error": None}
        if st == "failed":
            return {"status": "failed", "output": None, "error": d.get("error", "")}
        return {"status": "pending", "output": None, "error": None}

    def upload(self, path):
        return atlas_cloud.upload(path)

    def download(self, url, dest):
        return atlas_cloud.download(url, dest)

    def transcribe(self, audio, **params):
        return atlas_cloud.transcribe(audio, **params)


_REGISTRY = {"bailian_cli": BailianCliProvider, "bailian": BailianCliProvider,
             "bl": BailianCliProvider, "atlas_cloud": AtlasCloudProvider}


def get_provider(name=None):
    """Return a provider instance.  Bailian CLI is the default backend."""
    name = (name or "bailian_cli").lower()
    if name not in _REGISTRY:
        raise ProviderError(f"unknown provider '{name}'; available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]()


def run_jobs(prov, specs, *, poll_s=3, stall_s=90, max_retries=2, deadline_s=900):
    """Submit and poll a batch, resubmitting failed or stalled jobs."""
    if not specs:
        return {}
    limit = prov.max_parallel or len(specs)
    waiting = list(specs)
    st = {}

    def fill_slots():
        while waiting and len(st) < limit:
            key = waiting.pop(0)
            st[key] = {"pid": specs[key](), "t": time.time(), "tries": 0}
            print(f"[{key}] submitted {st[key]['pid']}")

    fill_slots()

    done = {}
    deadline = time.time() + deadline_s
    while len(done) < len(specs) and time.time() < deadline:
        time.sleep(poll_s)
        now = time.time()
        for key in list(st):
            submit = specs[key]
            s = st[key]
            r = prov.get_status(s["pid"])
            status = r["status"]
            if status == "completed":
                done[key] = r["output"]
                print(f"[{key}] done")
                del st[key]
            elif status == "failed" or (
                status == "pending" and now - s["t"] > stall_s
                and prov.supports_stall_resubmit
            ):
                if s["tries"] < max_retries:
                    s["tries"] += 1
                    s["pid"] = submit()
                    s["t"] = time.time()
                    why = "failed" if status == "failed" else f"stalled>{int(stall_s)}s"
                    print(f"[{key}] {why} -> resubmit #{s['tries']} ({s['pid']})")
                elif status == "failed":
                    done[key] = None
                    print(f"[{key}] FAILED: {(r.get('error') or '')[:1200]}")
                    del st[key]
        fill_slots()
    for key in specs:
        done.setdefault(key, None)
    return done
