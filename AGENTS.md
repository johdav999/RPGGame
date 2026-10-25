# RPGGame repository guidance

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
- Generated content requires scale/material/complexity and usage-rights review
  before moving from ignored `assets/generated` into versioned asset directories.
