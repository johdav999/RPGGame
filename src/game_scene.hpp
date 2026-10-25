#pragma once
#include "engine/scene.hpp"
#include "engine/camera_component.hpp"
#include <memory>

namespace rpg {
struct GameScene {
    std::unique_ptr<engine::Scene> scene;
    engine::ComponentId camera;
};
GameScene createGameScene();
}
