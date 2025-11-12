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
