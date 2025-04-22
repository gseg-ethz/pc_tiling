cmake_minimum_required(VERSION 3.24)
project(pc_tiling VERSION 1.0 LANGUAGES C CXX)

# ──────────────────────── Global options ─────────────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
enable_language(C)

# ──────────────────────── Dependencies ───────────────────────────────
find_package(PCL 1.8 REQUIRED)
find_package(Boost REQUIRED COMPONENTS filesystem)
find_package(OpenMP)
find_package(Python3 3.9 REQUIRED COMPONENTS Development)
find_package(SWIG 4.2 REQUIRED)
include(${SWIG_USE_FILE})

# ──────────────────────── Core C++ library ───────────────────────────
add_library(pc_tiling_cpp STATIC
    cpp/src/pc_tiling.cpp)

target_include_directories(pc_tiling_cpp
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/cpp/include>
        $<INSTALL_INTERFACE:include>
        ${PCL_INCLUDE_DIRS}
        ${Boost_INCLUDE_DIRS})

target_compile_options(pc_tiling_cpp PRIVATE
    -g -Wall -pedantic -Wextra -Wno-unused-parameter)

target_link_libraries(pc_tiling_cpp
    PUBLIC
        ${PCL_LIBRARIES}
        ${Boost_LIBRARIES})

if(OpenMP_CXX_FOUND)
    target_link_libraries(pc_tiling_cpp PUBLIC OpenMP::OpenMP_CXX)
endif()

# ── SWIG / Python module ─────────────────────────────────────────────
set(CMAKE_SWIG_OUTDIR "${CMAKE_CURRENT_SOURCE_DIR}/src/pc_tiling")

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/include
    ${PCL_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

# tell UseSWIG “this interface is C++”
set_source_files_properties(src/pc_tiling/pc_tiling.i
    PROPERTIES CPLUSPLUS ON)        # ← NEW, replaces -c++ hacks

swig_add_library(pc_tiling
    TYPE MODULE
    LANGUAGE python
    SOURCES src/pc_tiling/pc_tiling.i)


target_include_directories(pc_tiling PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/include
    ${PCL_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})
target_link_libraries(pc_tiling PRIVATE pc_tiling_cpp Python3::Python)

# ──────────────────────── Install rules (picked up by scikit‑build‑core) ──
install(TARGETS pc_tiling DESTINATION pc_tiling)       # goes into wheel
install(TARGETS pc_tiling_cpp ARCHIVE DESTINATION lib) # optional C++ lib
install(DIRECTORY cpp/include/ DESTINATION include)    # headers if wanted
