cmake_minimum_required(VERSION 3.14)
project(arithmetic_project LANGUAGES CXX)

# Build shared library libarithmetic.so
add_library(arithmetic SHARED arithmetic.cpp)
target_include_directories(arithmetic PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

set_target_properties(arithmetic PROPERTIES OUTPUT_NAME "arithmetic")

# install target for lib and headers
install(TARGETS arithmetic
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/arithmetic.h DESTINATION include)

# pybind11: fetch it
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.0
)
FetchContent_MakeAvailable(pybind11)

# wrapper module
pybind11_add_module(arithmetic_wrapper wrapper/arithmetic_pybind.cpp)
target_link_libraries(arithmetic_wrapper PRIVATE arithmetic)
target_include_directories(arithmetic_wrapper PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
set_target_properties(arithmetic_wrapper PROPERTIES OUTPUT_NAME "arithmetic")

# make wrapper target depend on lib build
add_dependencies(arithmetic_wrapper arithmetic)

# Helpful custom targets
add_custom_target(buildlib DEPENDS arithmetic)
add_custom_target(installlib
    COMMAND ${CMAKE_COMMAND} --build . --target install
    DEPENDS arithmetic
)
add_custom_target(wrapper ALL DEPENDS arithmetic_wrapper)

# pkg target: build lib + wrapper, then build a Python wheel
add_custom_target(pkg ALL
  COMMENT "Build lib, wrapper and package as a wheel"
)

# Ensure pkg depends on wrapper (which depends on arithmetic)
add_dependencies(pkg arithmetic_wrapper)

# After build, run a packaging step to copy the .so into python/arithmetic_pkg and build wheel
add_custom_command(TARGET pkg
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E echo "Packaging Python wheel..."
  COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/python/dist || true
  COMMAND ${CMAKE_COMMAND} -E chdir ${CMAKE_CURRENT_SOURCE_DIR} ${PYTHON_EXECUTABLE} -m pip install --upgrade pip setuptools wheel
  COMMAND ${CMAKE_COMMAND} -E chdir ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_COMMAND} -E echo "Searching for built extension..."
  # note: we rely on the wrapper having been built into the build directory; use a shell find in CI/local packaging
)
