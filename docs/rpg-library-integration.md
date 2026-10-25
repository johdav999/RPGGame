# Planned WebEngine RPG library integration

The reusable RPG library is planned in WebEngine, following its optional Modules
and Quests SDK pattern. This document records RPGGame's boundary; it does not add
runtime functionality or change the currently pinned engine revision.

Authoritative engine documents:

- [RPG library architecture](https://github.com/johdav999/WebEngine/blob/main/docs/rpg-library-architecture.md)
- [Ten release-1 implementation prompts](https://github.com/johdav999/WebEngine/blob/main/docs/rpg-library-release-1-prompts.md)

## Engine and game responsibilities

| Planned WebEngine mechanism | Shattered Sea responsibility |
| --- | --- |
| Character attributes, resources, modifiers and progression transactions | Backgrounds, stat definitions, coherence rules, XP curves and unlocks |
| Inventory, stacks, ownership, equipment and atomic transfers | Item catalogue, loot, prices, slots, ships/cargo and trade policy |
| Ability/effect evaluation and bounded status handling | Lattice probability distance, resonance, Unmaking risks, spells and balance |
| Turn order, action/movement budgets, command validation and reactions | Initiative/AP tuning, encounter composition, victory/escape, AI decisions and spatial queries |
| Optional integration with existing Quests and award receipts | Story acts, authored quests, dialogue, journal, factions and campaign consequences |
| Versioned RPG snapshots and validated restore | Combined campaign save, migrations, checkpoints, filesystem storage and recovery |
| Read-only state and committed action results | Third-person camera, targeting, animation, HUD, accessibility and audio |

The archipelago, sailing, route changes, crews, faction beliefs, Architects,
Gifted, Lattice and Unmaking stay here. ElevenLabs and Tripo remain authoring
tools. Generic means configurable mechanisms; it does not mean moving the game's
chosen rules or content into the engine.

## Planned composition

`GameSession` will own an `engine::rpg` runtime, an existing quest runtime and the
game's campaign/world state. It will retain immutable catalogues and compiled
game-policy registrations for their full lifetime. `WebEngine::RPG` is a proposed
portable target; `WebEngine::RPGQuests` is its separately optional quest bridge.
These targets do not yet exist in the pinned engine.

The host translates input/AI into typed commands and projects committed state
through existing engine scenes, camera, animation and audio. Scene bindings map
durable game IDs to transient engine handles and are rebuilt after load/travel.
The engine owns generic validation and transactions; this game supplies spatial
queries, destination reservation, rules and campaign effects. Turn decisions do
not advance with wall time, and animation does not apply damage twice.

Proposed code ownership when implementation starts:

- `src/app`: session composition and coordinated publication.
- `src/gameplay`: game definitions and compiled Lattice/combat policy.
- `src/world` and `src/narrative`: archipelago, campaign, story and faction state.
- `src/runtime`: scene bindings, queries and movement presentation.
- `src/presentation`: third-person controls, HUD, audio and visual feedback.
- `src/persistence`: outer save and migrations combining RPG, quest and campaign state.

These are planned paths; the current game still contains its starter scene.
Adopt a published engine release only after standalone native/Wasm, browser and
Windows sample gates pass. Then enable public targets and extend the existing
Linux cloud and Windows tests with game-specific policies and save/reward cases.
Do not copy engine sources or introduce a second scheduler. The first adoption
slice should prove one character, inventory, encounter and quest award in Greywake;
world-scale content and full campaign production follow separately.
