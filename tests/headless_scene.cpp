#include "game_scene.hpp"
#include "engine/application.hpp"
#include <iostream>
#include <stdexcept>
#include <utility>

namespace {
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
}

int main() {
    try {
        engine::Application app;
        auto initial = rpg::createGameScene();
        const auto camera = initial.camera;
        const auto first = app.loadScene(std::move(initial.scene));
        app.start(first);
        require(dynamic_cast<engine::CameraComponent*>(app.activeScene()->findComponent(camera)) != nullptr,
                "Game camera must remain resolvable after scene activation");
        app.advance(0.0);
        app.advance(0.02);
        require(app.clocks().simulation.delta > 0, "Active scene must advance simulation");
        require(app.activeScene()->collect().meshCount > 0, "Game scene must submit drawable geometry");

        app.pause();
        const auto pausedSeconds = app.clocks().simulation.seconds;
        app.advance(0.04);
        app.advance(0.06);
        require(app.clocks().simulation.seconds == pausedSeconds,
                "Paused game must preserve simulation time");
        app.resume();
        app.advance(0.08);
        app.advance(0.10);
        require(app.clocks().simulation.seconds > pausedSeconds, "Resume must restore simulation");

        auto replacement = rpg::createGameScene();
        const auto nextCamera = replacement.camera;
        const auto next = app.loadScene(std::move(replacement.scene));
        app.requestTransition(next, true);
        require(app.commitTransition(), "Replacement game scene must activate");
        require(app.activeSceneId() == next && app.findScene(first) == nullptr,
                "Transition must retire the previous scene");
        require(app.activeScene()->findComponent(nextCamera) != nullptr,
                "Replacement scene must expose its own camera");
        app.advance(0.12);
        app.shutdown();
        require(app.state() == engine::ApplicationState::Stopped && app.loadedSceneCount() == 0,
                "Shutdown must release game scenes");
        std::cout << "Headless game scene lifecycle passed\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
