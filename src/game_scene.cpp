#include "game_scene.hpp"
#include "engine/mesh_component.hpp"
#include "engine/light_component.hpp"

namespace rpg {
GameScene createGameScene() {
    using namespace engine;
    auto scene = std::make_unique<Scene>("RPG starter clearing");
    scene->ambient = {.12f, .15f, .18f};
    auto& camera = scene->spawn("Game camera").addComponent<CameraComponent>();
    camera.transform.position = {10, 8, 12};
    camera.lookAt({0, 1, 0});
    camera.farPlane = 200;

    auto& sun = scene->spawn("Sun").addComponent<LightComponent>("Sun", LightType::Directional);
    sun.direction = {-.6f, -1, -.4f};
    sun.intensity = 2;
    sun.shadow.enabled = true;
    sun.shadow.halfExtent = 20;
    sun.shadow.halfDepth = 40;

    auto object = [&](const char* name, Vec3 position, Vec3 scale, Vec3 color) {
        auto material = std::make_shared<Material>();
        material->baseColor = color;
        material->roughness = .8f;
        auto& mesh = scene->spawn(name).addComponent<MeshComponent>(name, Mesh::cube());
        mesh.transform.position = position;
        mesh.transform.scale = scale;
        mesh.color = {1, 1, 1};
        mesh.setMaterial(0, MaterialInstance{material});
    };
    object("Ground", {0, -.25f, 0}, {20, .5f, 20}, {.22f, .35f, .19f});
    object("Player placeholder", {0, 1, 0}, {.8f, 2, .8f}, {.2f, .45f, .8f});
    object("Landmark", {-4, 1.5f, -3}, {2, 3, 2}, {.45f, .42f, .38f});
    const auto cameraId = camera.id();
    return {std::move(scene), cameraId};
}
}
