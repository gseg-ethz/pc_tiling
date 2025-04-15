# PC Tiling

PC Tiling is a high-performance point cloud processing library implemented in C++ and made available to Python using 
SWIG. It leverages the [Point Cloud Library (PCL)](https://pointclouds.org/) for robust point cloud segmentation, 
filtering, and tiling. This package enables you to easily split large point cloud datasets into smaller, manageable 
tiles and apply voxel grid filtering to standardize resolution.

## Features

- **Point Cloud Tiling:** Automatically splits point clouds into tiles based on spatial boundaries.
- **Voxel Grid Filtering:** Uniformly down-samples point clouds to improve computational performance.
- **Resaving Functionality:** Offers functions to load and resave PLY-formatted point clouds.
- **PCL Integration:** Utilizes PCL’s efficient segmentation, filtering, and feature estimation techniques.
- **Parallel Processing:** Supports parallel computation using OpenMP for faster performance.

## Requirements

- **Python:** Python 3.11
- **C++ Compiler:** Must support C++17
- **CMake:** Version 3.10 or higher
- **SWIG:** Version 3.0 or higher (for Python binding generation)
- **PCL:** Point Cloud Library, version 1.8 or higher
- **Boost:** Including the filesystem component
- **OpenMP:** Available with your C++ compiler (optional but recommended)

## Installation

### Prerequisites

Ensure you have the following dependencies installed:

- **CMake:**  
  See [cmake.org](https://cmake.org/download/) for download instructions.
- **SWIG:**  
  On Ubuntu, install with:  
  ```bash
  sudo apt-get install swig
  ```
- **PCL:**  
  Follow the [official PCL installation guide](https://pointclouds.org/downloads/) for your platform.
- **Boost:**  
  On Ubuntu:  
  ```bash
  sudo apt-get install libboost-all-dev
  ```
- **Python Development Headers:**  
  On Ubuntu:  
  ```bash
  sudo apt-get install python3-dev
  ```

### Building and Installing

The installation process will automatically build the shared library and generate the SWIG bindings. Simply run:

```bash
pip install .
```

This command will:
- Build the C++ shared library using CMake (placing it in the `lib` folder).
- Generate the SWIG wrapper (`pc_tiling_wrap.cxx`).
- Place all components in the proper locations for Python to import the module.

## Usage

After installation, you can import the module in your Python projects. Here’s a simple example that demonstrates how to 
use the tiling functionality:

```python
import pc_tiling

# Define the input point cloud files (PLY format)
first_cloud_path = 'path/to/first/point_cloud.ply'
second_cloud_path = 'path/to/second/point_cloud.ply'

# Define the directory to save the tiling results
results_dir = 'path/to/save/results'

# Tiling configuration parameters
max_points = 100000        # Maximum number of points per tile
min_points = 1000          # Minimum number of points per tile
voxel_flag = True          # Enable voxel grid filtering
voxel_size = 0.05          # Size of the voxel grid filter (in meters)
overlap = 20.0             # Overlap size for tiling (in meters)
projection_axis = -1       # Set to -1 to auto-select axis based on overlap 
verbose = True             # Enable verbose logging

# Perform the tiling operation
if pc_tiling.tile_point_clouds(first_cloud_path, second_cloud_path, results_dir,
                               max_points, min_points, voxel_flag, voxel_size,
                               overlap, projection_axis, verbose):
    print("Tiling completed successfully!")
else:
    print("An error occurred during tiling.")
```

## API Overview

The main functions available in the module are:

- **`tile_point_clouds(...)`**  
  Splits point clouds into tiled patches based on the specified parameters.  
  *Parameters include*:  
  - `firstPointCloud`: Path to the first point cloud file.
  - `secondPointCloud`: Path to the second point cloud file.
  - `resultsPath`: Directory where tiled outputs will be saved.
  - `maxPointsPerTile`: Maximum allowed points per tile.
  - `minPointsPerTile`: Minimum required points per tile.
  - `voxelGridFlag`: A boolean flag to enable voxel grid filtering.
  - `voxelGridFilterSize`: The voxel grid filter size.
  - `overlapTiles`: The amount of overlap between tiles.
  - `projectionDirection`: Axis for projecting the point clouds (0 for X, 1 for Y, 2 for Z, or -1 for automatic selection).
  - `verbose`: Enable or disable verbose output.

- **`resave_point_cloud(...)`**  
  Resaves the input point cloud files (PLY format) after reading them.

## License

This project is licensed under the [Your License Name] license. See the LICENSE file for more details.

## Contributing and Support

If you have any issues or suggestions, please feel free to submit an issue or a pull request in the repository.

For questions, please contact the project maintainers.
```
