import bpy

####################################################################################################
filename="world_file.dat"
title="[World Data]"
world_layer=0
####################################################################################################

filename = bpy.path.abspath("//") + filename
obj_list=[]

for ob in bpy.data.objects:
    if ob.layers[world_layer]:
        obj_list.append(ob)

target_file=open(filename, 'w')
target_file.write(title)
target_file.write("\n")

for i in obj_list:
    target_file.write("object_name=")
    target_file.write(str(i.name))
    target_file.write("\n")
    
    target_file.write("mesh=")
    target_file.write(str(i.data.name))
    target_file.write("\n")
    target_file.write("object_coords=")
    for a in range(0, 2):
        target_file.write(str(i.location[a]))
        target_file.write(" ")
    target_file.write("\n")
    target_file.write("object_scale=")
    for a in range(0, 2):
        target_file.write(str(i.scale[a]))
        target_file.write(" ")
    target_file.write("\n")
    target_file.write("object_rotation=")
    for a in range(0, 2):
        target_file.write(str(i.rotation_euler[a]))
        target_file.write(" ")
    target_file.write("\n")
    target_file.write("\n")
    
print("Done!")