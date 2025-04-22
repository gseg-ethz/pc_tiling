#ifndef PC_TILING_H
#define PC_TILING_H

#include <string>

bool tile_point_clouds(std::string firstPointCloud,
					   std::string secondPointCloud,
					   std::string resultsPath,
					   int maxPointsPerTile,
					   int minPointsPerTile,
					   bool voxelGridFlag,
					   float voxelGridFilterSize,
					   float overlapTiles,
					   int projectionDirection,
					   bool verbose);


bool resave_point_cloud(std::string firstPointCloud,
					   std::string secondPointCloud,
					   bool verbose);

#endif // PC_TILING_H