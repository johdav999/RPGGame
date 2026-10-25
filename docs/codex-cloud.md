# Codex cloud development

Cloud tasks can compile the actual game scene and run its application lifecycle
tests on Linux. The playable desktop game still uses Windows x64, MSVC and D3D12.
Cloud validation does not open a game window or verify graphics, audio or input.

## Prepare an environment

In Codex, open **Settings > Codex Cloud > Environments > Create environment**,
select `johdav999/RPGGame`, and choose a Linux environment with Git, a C++20
compiler (GCC 13 or newer recommended), CMake 3.24+, Ninja and Python 3.12+.
On Ubuntu the build packages are `build-essential cmake ninja-build git python3`.
Install missing packages during environment preparation using its package manager.

Use this repository-root command as the environment's Install script:

```bash
bash scripts/setup-cloud.sh
```

It initializes the pinned WebEngine submodule, configures the headless build,
fetches the hash-pinned Jolt source, builds and runs C++ integration tests and
offline Python tests. It fails immediately on missing prerequisites or errors.
The default build parallelism is two jobs to limit memory; set
`CMAKE_BUILD_PARALLEL_LEVEL` to adjust it for the environment's resources.

Preparation needs access to GitHub for the submodule and `codeload.github.com`
for Jolt, plus the selected OS package repositories if installing prerequisites.
Grant GitHub access to both RPGGame and WebEngine if repository permissions
require it. No ElevenLabs or Tripo credentials are needed for builds or tests.

Review the successful preparation output and **Publish** the environment. Select
it when starting a cloud task. Publishing an account environment is a separate
UI step; committing these files does not create or publish one automatically.
Rebuild and republish the environment after engine pin or prerequisite changes.

The current product workflow is documented in
[Codex cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments).

## Commands inside a task

```bash
bash scripts/check-cloud.sh
```

This reconfigures, builds and tests against the current task checkout. Prepared
dependency sources under `build/cloud/_deps` allow routine checks without
provider access. If the engine pin or dependency definitions change, run setup
with network access again; do not advance the submodule to its latest branch.

The `cloud` preset disables `RPG_BUILD_DESKTOP`, enables `RPG_BUILD_TESTS` and
builds `rpg_headless_tests`. The shared `rpg_scene` library is also used by the
Windows executable, so this validates game source rather than a cloud-only mock.
The tests cover camera resolution, drawable scene collection, simulation
pause/resume, scene replacement and shutdown. They do not establish that the
planned third-person controls or turn-based combat have been implemented.

## Task guidance and validation

`AGENTS.md` supplies task instructions automatically from the repository. Keep
portable game code free of Windows headers; select the platform in desktop
composition. Add meaningful rule and integration coverage as gameplay develops.

GitHub Actions runs Linux headless checks and a Windows Release build on pushes
and pull requests. Changes to C++ or CMake need both. Check actual rendering on
a Windows GPU separately. Asset generation remains an explicit authoring step;
never call paid providers from environment setup, tests or CI.

Example task prompt:

> Implement the next scoped gameplay change using docs/game-design.md and
> docs/architecture.md. Follow AGENTS.md, run bash scripts/check-cloud.sh, and
> report Windows or GPU validation that still needs to run.
