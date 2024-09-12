cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(pc_tiling VERSION 1.0 LANGUAGES C CXX)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include own headers
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../include)

# Add the source file
add_library(pc_tiling SHARED ${CMAKE_CURRENT_SOURCE_DIR}/pc_tiling.cpp)

target_compile_options(pc_tiling PRIVATE -g -Wall -pedantic -Wextra -Wno-unused-parameter -fPIC)

# Find and include PCL package
find_package(PCL 1.8 REQUIRED)
find_package(Boost REQUIRED COMPONENTS filesystem)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Include PCL and Boost headers
target_include_directories(pc_tiling SYSTEM PUBLIC ${PCL_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

# Link against PCL libraries and Boost Filesystem
target_link_libraries(pc_tiling PRIVATE ${PCL_LIBRARIES} ${Boost_LIBRARIES})

# Find and set up OpenMP if available
find_package(OpenMP REQUIRED)
if(OPENMP_FOUND)
  message("OPENMP FOUND")
  target_compile_options(pc_tiling PRIVATE ${OpenMP_C_FLAGS} ${OpenMP_CXX_FLAGS})
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

# Set the library output directory
set_target_properties(pc_tiling PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)
