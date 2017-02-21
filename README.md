# Blender world file
This is a python script that automatically writes the name of an object, coordinates, scale and rotation of all objects on a specific layer in a Blender file.

# How to use:
Open your .blend file in Blender and open a text editor or just change the layout to "Scripting" (bar at the top). Click "Open" and select the script.
Adjust the parameters to your needs. The world file will be written in the same directory as the .blend file and title is the header of the file.
world_layer is the layer with the objects to be written in the output file. Note that it is zero-based, so layer one is world_layer=0.

##Sample output:
```
[World Data]
object_name=ball4
object_coords=-1.4219375848770142 -4.805078983306885 1.1102250814437866
object_scale=0.4466085433959961 0.4466085433959961 0.4466085433959961
object_rotation=0.0 0.0 0.0

object_name=box1
object_coords=-2.1695494651794434 3.764418363571167 2.4148027896881104
object_scale=1.3081520795822144 1.3081520795822144 1.3081519603729248
object_rotation=-0.41686466336250305 -0.06108555942773819 -0.41660451889038086

object_name=wall
object_coords=0.0 0.0 0.0
object_scale=3.9948277473449707 3.9948277473449707 3.9948277473449707
object_rotation=1.5707963705062866 -0.0 0.0
```

The coordinates are in the order XYZ for Blender, which means that positive Z is upwards, so it has to be swapped with Y for most coordinate systems.
The rotation is in degrees, in the same order and with Z and Y swapped.

The idea is that this file can be parsed by a game and the attributes for the in-game objects will be read from the file.
