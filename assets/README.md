# Game assets

Generated content is local under `generated/audio` and `generated/models` and is
ignored until reviewed. Keep approved content in `audio/`, `models/`, `textures/`
and `scenes/`. The build copies this directory beside the executable.

Use GLB for models, meters for scale and Y-up orientation. Verify scale, pivot,
materials, mesh complexity, collisions and animation before runtime integration.
Use WAV for short sound effects; MP3 is supported by the native music streaming
path. Generated files are not loaded automatically by the starter scene.

Keep prompt, provider/model version, generation date and usage-rights notes with
each approved asset. Do not commit API responses containing temporary download URLs.
