# RPGGame repository guidance

- Read `docs/architecture.md` before changing system boundaries, ownership,
  gameplay execution, world loading or persistence. Keep its implemented/planned
  status accurate as the game develops.
- This is a 3D Windows desktop RPG using the pinned `external/WebEngine` submodule.
- Link the engine's public CMake targets. Keep gameplay, content and save policy
  here; do not copy private renderer or platform implementation files.
- DesktopHost owns the Application, input dispatch and frame advance. Register
  camera views before scene activation; honor GUI-consumed events and callback lifetimes.
- Do not modify or advance the engine submodule without a task requiring it.
- Keep ElevenLabs/Tripo generation in authoring tools; credentials come from the
  environment and must never be embedded in the runtime, committed or logged.
- Run `python -m unittest discover -s tests -v` for asset-tool changes and a
  Windows Release build for C++/CMake changes. Record GPU/runtime checks separately.
- In Linux/Codex cloud, first run `bash scripts/setup-cloud.sh` if the environment
  is unprepared, then use `bash scripts/check-cloud.sh` for task validation.
  See `docs/codex-cloud.md` for prerequisites and environment preparation.
  Cloud tests compile the shared game scene without the Windows renderer;
  use Windows CI for the desktop build and report GPU checks as unverified.
- Keep portable scene/game code in shared targets. `RPG_BUILD_DESKTOP` controls
  native Windows composition; `RPG_BUILD_TESTS` controls game tests independently
  of the engine's `BUILD_TESTING`. Do not enable paid generation in setup or CI.
- Generated content requires scale/material/complexity and usage-rights review
  before moving from ignored `assets/generated` into versioned asset directories.
