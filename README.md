# Parsable map files from Blender scenes
This is a python script that takes information about objects from a .blend file and writes it out into a parsable format to use in games.
The program outputs two files: one with basic information about the objects which contains:

 - object name
 - mesh name to import the right .obj file
 - object translation
 - object rotation
 - object scale
 - TODO: texture path
 - if the object is an empty and its name begins with "spawn", its translation will be included in a dedicated section in the map file

And another file which is just a skeleton file to manually add other attributes to the object. These attributes are in a separate file because the first file will probably be regenerated multiple times, but the manually added information should not be overwritten in that process.

# How to use:
Execute `generate_world_file.py` (python 3) with the following arguments:

 - path to the .blend file to build the map from
 - `--output`: the path where the map directory will be created (default: cwd)
 - `--layer`: the layer in blender where the map objects are located (default: 0)
 - `--actions`: if specified, an empty boilerplate file for extra attributes will be generated
 - `--no-spawns`: if specified, spawn points will not be included in the file

#Sample output:
```
<World name in header>

{objects}

[Object 1]
model=mymodel.obj
translation=0.451,45.23,100.4
rotation=1.7,0.5,0.234
scale=2,2,2
tex_diff=mat/wood1_col.png
tex_spec=mat/wood1_spec.png
tex_nrm=mat/wood1_nrm.png
[/Object 1]


[platform big center]
model=mymodel.obj
translation=0.451,45.23,100.4
rotation=1.7,0.5,0.234
scale=2,2,2
tex_diff=mat/wood1_col.png
tex_spec=mat/wood1_spec.png
tex_nrm=mat/wood1_nrm.png
[/platform big center]

{/objects}

{spawnpoints}

[spawn1]
translation=0.5,5.6,10
[/spawn1]

[spawn2]
translation=0.5,5.6,10
[spawn2]

{/spawnpoints}
```

The coordinates are in the order XYZ for Blender, which means that positive Z is upwards, so it has to be swapped with Y for most coordinate systems.
The rotation is in degrees, in the same order and with Z and Y swapped.

The idea is that this file can be parsed by a game and the attributes (animations...) for the in-game objects will be read from the generated files.
