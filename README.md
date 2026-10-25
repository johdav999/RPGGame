# RPGGame

Game concept: [The Shattered Sea](docs/game-concept.md), a quantum-fantasy RPG
set across an archipelago shaped by ancient technology and unstable reality.

Technical design: [Game architecture](docs/architecture.md), including system
boundaries, world streaming, Lattice rules, persistence and delivery stages.

Shared-library plan: [WebEngine RPG integration](docs/rpg-library-integration.md),
separating reusable RPG mechanisms from Shattered Sea rules and content.

Playable design: [Game design document](docs/game-design.md), covering player
experience, mechanics, progression, art direction and the Greywake opening slice.

A C++20 foundation for a **3D RPG on Windows x64**, using
[WebEngine](https://github.com/johdav999/WebEngine)'s native desktop runtime and
renderer. The engine is a pinned Git submodule, not a copied renderer or browser
wrapper. The game builds the engine's direct D3D12 renderer. Game rules belong
in this repo.

The starter displays a lit 3D clearing with ground, a player placeholder and a
landmark. Escape quits and F11 toggles fullscreen. Movement, combat, quests,
inventory and loading generated assets are future game work.

## Build and run

Install Git, Visual Studio 2022 with **Desktop development with C++**, the Windows
SDK, CMake 3.24+ and Python 3.12+. Then use PowerShell:

```powershell
git clone --recurse-submodules https://github.com/johdav999/RPGGame.git
cd RPGGame
./scripts/setup-windows.ps1
./scripts/build-windows.ps1
./build/windows/bin/Release/rpg_game.exe
```

Setup installs the engine's hash-verified SDL3, Dawn and DirectX Shader Compiler
packages locally; the engine setup includes Dawn, but this game builds only
direct D3D12. The pinned engine's optional Dawn renderer currently hits MSVC's
shader string-literal size limit. CMake also fetches pinned physics/navigation
dependencies. The first setup needs internet access. Build outputs and SDKs are
ignored. `CMakeUserPresets.json` is available for local toolchain overrides.
The build stages SDL and DXC DLLs and assets beside the executable. This is a
development build; a redistributable installer, dependency-license bundle,
publisher signing and clean-machine validation still need a release workflow.

## Codex cloud tasks

The repository also supports Linux headless development. Prepare a Codex cloud
environment with `bash scripts/setup-cloud.sh`, then run
`bash scripts/check-cloud.sh` inside tasks. This compiles the shared game scene
and tests its lifecycle without a GPU. See [cloud setup](docs/codex-cloud.md) for
prerequisites, network access and the environment publishing step. The playable
Windows renderer continues to be checked by Windows CI and local GPU testing.

## ElevenLabs audio and Tripo 3D

Python authoring tools generate local assets ahead of time. The game contains no
provider credentials or generation SDK. Set credentials in your shell; the
`.env.example` file lists settings but is not automatically loaded:

```powershell
$env:ELEVENLABS_API_KEY = '<your key>'
$env:ELEVENLABS_VOICE_ID = '<your voice id>'
$env:TRIPO_API_KEY = '<your key>'

# Inspect requests for free, without credentials or network calls:
python tools/generate_assets.py speech --text "Welcome, traveler." --dry-run
python tools/generate_assets.py model --prompt "A weathered stone arch, game prop" --dry-run

# These commands use provider credits:
python tools/generate_assets.py speech --text "Welcome, traveler." --output assets/generated/audio/welcome.mp3
python tools/generate_assets.py model --prompt "A weathered stone arch, game prop" --output assets/generated/models/arch.glb
# Resume a printed task ID after interruption without paying for a new task:
python tools/generate_assets.py model-result --task-id task_123 --output assets/generated/models/arch.glb

python -m unittest discover -s tests -v
```

ElevenLabs currently generates dialogue MP3s; additional sound-effect/music
authoring can be added separately. Tripo creates a text-to-model task, polls with
a timeout and downloads the GLB on success. Provider/model IDs are configurable
through `.env.example`'s environment settings or `--model`. Existing output files
are protected from overwrite. Downloads never receive the Tripo API key.
Generated assets stay ignored until reviewed; see [asset conventions](assets/README.md).
Generation is never run during builds or CI. Live API calls require your own
accounts, credentials and credits.

Provider references:
[ElevenLabs speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert),
[Tripo API quick start](https://developers.tripo3d.ai/en/docs/quick-start).

## Repository workflow

`origin` is [johdav999/RPGGame](https://github.com/johdav999/RPGGame).
GitHub Actions checks the offline authoring tools and builds the native Windows
executable on pushes and pull requests. GPU rendering acceptance requires a
Windows machine; CI compilation is not a graphics test.

Update the engine deliberately: check out a reviewed commit in `external/WebEngine`,
build/test the game, then commit the changed submodule pointer. Keep engine
implementation changes in the engine repository. Do not commit `.env`, API keys,
generated caches, SDKs or temporary provider download URLs. Review large approved
assets before choosing Git LFS or a separate content distribution store.
