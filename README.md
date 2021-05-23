# Voronoi Dungeon Generation Algorithm

This repository provides dungeon generation algorithm using voronoi diagram.

# Generation Steps and examples

## Step 1

Randomly set points which have some distance from each other and from walls.

![Step_1](./Sample/Step_1.png)

## Step 2

Find the nearest randomly selected point using Manhattan distance for the entire pixel and add the pixel to that point’s room.

![Step_2](./Sample/Step_2.png)

## Step 3

Empty the pixel with same distance from multiple points for making wall.

![Step_3](./Sample/Step_3.png)



## Step 4

Find set of neighbors, and randomly select one of them. Connect two rooms and append the rooms to the group. Until group has every member of the rooms, select new path from set of neighbors which contains at least one member from group. If a path is selected, append new rooms to the group.

![Step_4](./Sample/Step_4.png)