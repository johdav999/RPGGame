cmake_minimum_required(VERSION 3.24)
project(RPGGame VERSION 0.1.0 LANGUAGES C CXX)

if(NOT WIN32 OR NOT MSVC OR NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
  message(FATAL_ERROR "RPGGame requires Windows x64 and the MSVC C++ toolchain.")
endif()
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# Dependency package targets must remain visible for app-local DLL staging.
set(CMAKE_FIND_PACKAGE_TARGETS_GLOBAL TRUE)
set(WEBENGINE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external/WebEngine")
if(NOT EXISTS "${WEBENGINE_SOURCE_DIR}/CMakeLists.txt")
  message(FATAL_ERROR "Run git submodule update --init --recursive before configuring.")
endif()
set(BUILD_TESTING OFF CACHE BOOL "Build dependency tests")
set(WEBENGINE_BUILD_WINDOWS ON CACHE BOOL "Native Windows host" FORCE)
set(WEBENGINE_WINDOWS_D3D12 ON CACHE BOOL "Native D3D12 renderer" FORCE)
set(WEBENGINE_WINDOWS_DAWN OFF CACHE BOOL "Use the native D3D12 renderer only" FORCE)
add_subdirectory(external/WebEngine build-engine EXCLUDE_FROM_ALL)

add_executable(rpg_game src/main.cpp src/game_scene.cpp)
target_include_directories(rpg_game PRIVATE src)
target_link_libraries(rpg_game PRIVATE WebEngine::Desktop WebEngine::WindowsRuntime)
target_compile_options(rpg_game PRIVATE /W4 /utf-8)
set_target_properties(rpg_game PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

# Stage only the runtime needed by this game, without building engine demos.
add_custom_command(TARGET rpg_game POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "$<TARGET_FILE:SDL3::SDL3-shared>"
    "${WEBENGINE_DXC_DIR}/bin/x64/dxcompiler.dll"
    "${WEBENGINE_DXC_DIR}/bin/x64/dxil.dll"
    "$<TARGET_FILE_DIR:rpg_game>"
  COMMAND ${CMAKE_COMMAND} -E copy_directory
    "${CMAKE_CURRENT_SOURCE_DIR}/assets" "$<TARGET_FILE_DIR:rpg_game>/assets"
  VERBATIM)
