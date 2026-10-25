#include "game_scene.hpp"
#include "engine/desktop.hpp"
#include <iostream>
#include <stdexcept>
#include <string_view>

int main(int argc, char** argv) {
    try {
        engine::DesktopSettings settings;
        settings.title = "RPGGame | WebEngine";
        settings.backend = engine::DesktopBackend::Direct3D12;
        for (int i = 1; i < argc; ++i) {
            const std::string_view arg = argv[i];
            if (arg == "--help") {
                std::cout << "RPGGame [--backend d3d12|auto]\nEscape: quit; F11: fullscreen\n";
                return 0;
            }
            if (arg != "--backend" || ++i >= argc)
                throw std::invalid_argument("Use --backend d3d12|auto");
            const std::string_view backend = argv[i];
            if (backend == "d3d12") settings.backend = engine::DesktopBackend::Direct3D12;
            else if (backend == "auto") settings.backend = engine::DesktopBackend::Automatic;
            else throw std::invalid_argument("Unknown renderer backend");
        }
        engine::DesktopHost host(settings);
        auto game = rpg::createGameScene();
        const auto sceneId = host.application().loadScene(std::move(game.scene));
        const engine::DesktopView view{game.camera};
        host.setViews(sceneId, {&view, 1});
        host.application().start(sceneId);
        host.setEventHandler([&](const engine::DesktopEvent& event) {
            using namespace engine;
            if (event.type != DesktopEventType::Control || !event.down || event.repeat || event.guiConsumed)
                return false;
            if (event.control == DesktopControl::Escape) { host.requestClose(); return true; }
            if (event.control == DesktopControl::F11) { host.setFullscreen(!host.fullscreen()); return true; }
            return false;
        });
        return host.run();
    } catch (const std::exception& error) {
        std::cerr << "RPGGame: " << error.what() << '\n';
        return 1;
    }
}
