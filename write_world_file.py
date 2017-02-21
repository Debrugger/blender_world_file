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
        obj_list.append(ob.name)

target_file=open(filename, 'w')
target_file.write(title)
target_file.write("\n")

obj_counter=0

for i in obj_list:
    target_file.write("object_name=")
    target_file.write(str(i))
    target_file.write("\n")
    target_file.write("mesh=")
    target_file.write(str(bpy.data.objects[obj_counter].data.name))
    target_file.write("\n")
    target_file.write("object_coords=")
    target_file.write(str(bpy.data.objects[obj_counter].location[0]))
    target_file.write(" ")
    target_file.write(str(bpy.data.objects[obj_counter].location[1]))
    target_file.write(" ")
    target_file.write(str(bpy.data.objects[obj_counter].location[2]))
    target_file.write(" ")
    target_file.write("\n")
    target_file.write("object_scale=")
    target_file.write(str(bpy.data.objects[obj_counter].scale[0]))
    target_file.write(" ")
    target_file.write(str(bpy.data.objects[obj_counter].scale[1]))
    target_file.write(" ")
    target_file.write(str(bpy.data.objects[obj_counter].scale[2]))
    target_file.write(" ")
    target_file.write("\n")
    target_file.write("object_rotation=")
    target_file.write(str(bpy.data.objects[obj_counter].rotation_euler[0]))
    target_file.write(" ")
    target_file.write(str(bpy.data.objects[obj_counter].rotation_euler[1]))
    target_file.write(" ")
    target_file.write(str(bpy.data.objects[obj_counter].rotation_euler[2]))
    target_file.write(" ")
    target_file.write("\n")
    target_file.write("\n")
    obj_counter += 1
    
print("Done!")