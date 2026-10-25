"""Offline asset authoring clients; never imported by the shipped game.

Uses Python's standard library. Credentials come only from environment variables.
Generation commands make billable requests unless --dry-run is supplied.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def request(url, *, payload=None, headers=None, binary=False):
    data = json.dumps(payload).encode() if payload is not None else None
    merged = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=merged)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read()
    except urllib.error.HTTPError as error:
        # Provider bodies/URLs may contain secrets or signed download links.
        raise RuntimeError(f"Provider returned HTTP {error.code}; check credentials, quota and request settings.") from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError("Provider request failed or timed out. Check the connection; generation may still be running.") from None
    return body if binary else json.loads(body)


def credential(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Set {name} in your shell before generating assets.")
    return value


def output_path(value, extension):
    path = Path(value)
    if path.suffix.lower() != extension:
        raise ValueError(f"Output must use {extension}.")
    if path.exists():
        raise ValueError("Output already exists; choose a new path.")
    return path


def write_asset(path, data):
    if not data:
        raise RuntimeError("Provider returned an empty asset.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(data)
    print(f"Saved {path}")


def tripo_call(route, payload=None):
    result = request("https://openapi.tripo3d.ai/v3/" + route,
                     payload=payload,
                     headers={"Authorization": "Bearer " + credential("TRIPO_API_KEY")})
    if result.get("code") != 0 or not isinstance(result.get("data"), dict):
        raise RuntimeError("Tripo rejected the request; check your account and model settings.")
    return result["data"]


def safe_task_id(value):
    if not value or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in value):
        raise ValueError("Invalid Tripo task ID.")
    return value


def wait_for_model(task_id, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        task = tripo_call("tasks/" + safe_task_id(task_id))
        status = task.get("status")
        if status == "success":
            url = task.get("output", {}).get("model_url", "")
            if urllib.parse.urlparse(url).scheme != "https":
                raise RuntimeError("Tripo returned no valid HTTPS model download.")
            # Signed asset downloads must not receive the provider API key.
            data = request(url, binary=True)
            if not data.startswith(b"glTF"):
                raise RuntimeError("Downloaded asset is not a GLB file.")
            return data
        if status in {"failed", "cancelled", "banned"}:
            raise RuntimeError(f"Tripo task {task_id} ended with status {status}.")
        if status not in {"queued", "running"}:
            raise RuntimeError(f"Unexpected Tripo status for task {task_id}; resume later.")
        time.sleep(min(2, max(0, deadline - time.monotonic())))
    raise RuntimeError(f"Timed out. Resume without creating another paid task: model-result --task-id {task_id}")


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)
    speech = commands.add_parser("speech", help="Generate ElevenLabs MP3 dialogue")
    speech.add_argument("--text", required=True)
    speech.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    speech.add_argument("--model", default=os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"))
    speech.add_argument("--output", default=str(ROOT / "assets/generated/audio/dialogue.mp3"))
    speech.add_argument("--dry-run", action="store_true")
    model = commands.add_parser("model", help="Create a Tripo text-to-GLB task")
    model.add_argument("--prompt", required=True)
    model.add_argument("--model", default=os.environ.get("TRIPO_MODEL", "v3.1-20260211"))
    model.add_argument("--dry-run", action="store_true")
    result = commands.add_parser("model-result", help="Resume/download an existing task without new generation")
    result.add_argument("--task-id", required=True, type=safe_task_id)
    for command in (model, result):
        command.add_argument("--output", default=str(ROOT / "assets/generated/models/model.glb"))
        command.add_argument("--timeout", type=int, default=600)
    return cli


def main(argv=None):
    cli = parser()
    args = cli.parse_args(argv)
    try:
        output = output_path(args.output, ".mp3" if args.command == "speech" else ".glb")
        if args.command == "speech":
            if not args.text.strip():
                raise ValueError("Speech text cannot be empty.")
            payload = {"text": args.text, "model_id": args.model}
            if args.dry_run:
                print(json.dumps({"provider": "elevenlabs", "payload": payload, "output": str(output)}))
                return 0
            if not args.voice_id:
                raise ValueError("Set ELEVENLABS_VOICE_ID or pass --voice-id.")
            voice_id = urllib.parse.quote(args.voice_id, safe="")
            data = request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
                           payload=payload, headers={"xi-api-key": credential("ELEVENLABS_API_KEY")}, binary=True)
        else:
            if args.timeout <= 0:
                raise ValueError("Timeout must be positive.")
            if args.command == "model":
                if not args.prompt.strip():
                    raise ValueError("Model prompt cannot be empty.")
                payload = {"prompt": args.prompt, "model": args.model}
                if args.dry_run:
                    print(json.dumps({"provider": "tripo", "payload": payload, "output": str(output)}))
                    return 0
                task_id = safe_task_id(tripo_call("generation/text-to-model", payload)["task_id"])
                print(f"Tripo task: {task_id}", flush=True)
            else:
                task_id = args.task_id
            data = wait_for_model(task_id, args.timeout)
        write_asset(output, data)
        return 0
    except (ValueError, RuntimeError, OSError, KeyError) as error:
        print(f"Asset generation: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
