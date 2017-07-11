import sys
import os
import argparse
import bpy

def write_objects(f, objects):
    f.write("{objects}\n")
    for i in objects:
        f.write("[%s]\n" % str(i.name)) #write object name header
        
        f.write("model=%s.obj\n" % str(i.data.name)) #.obj file
        f.write("translation=")
        for a in range(0, 3):
            f.write(str(i.location[a]))
            if a!=2:
                f.write(",")
        f.write("\n")

        f.write("scale=")
        for a in range(0, 3):
            f.write(str(i.scale[a]))
            if a!=2:
                f.write(",")
        f.write("\n")

        f.write("rotation=")
        for a in range(0, 3):
            f.write(str(i.rotation_euler[a]))
            if a!=2:
                f.write(",")
        f.write("\n\n")

        f.write("tex_diff=" + "\n")
        f.write("tex_spec=" + "\n")
        f.write("tex_nrm=" + "\n")

        f.write("[/%s]\n" % str(i.name))
        f.write("\n")
    f.write("{/objects}\n\n")

def write_spawns(f, spawns):
    f.write("{spawnpoints}\n")    
    for s in spawns:
        f.write("[%s]\n" % s.name)
        f.write("translation=")
        for a in range(0, 3):
            f.write(str(s.location[a]))
            if a!=2:
                f.write(",")
        f.write("\n\n")
        f.write("[/%s]\n" % s.name)
    f.write("{/spawnpoints}\n")

def write_action_boilerplate(filename, objects):
    f = open(filename, 'w')
    for o in objects:
        f.write("[%s]\n\n" % o.name)
        f.write("attributes=\n\n")
        f.write("-actions-\n\n")
        f.write("[/%s]\n\n" % o.name)
    f.close()

#create directories for map
def main():
    parser = argparse.ArgumentParser(description = "Generate an NST map data file from a scene in blender. This program is made to be executed from the Blender python environment.")
    parser.add_argument("--name", "-n", help = "name of the map", required = True)
    parser.add_argument("--output", "-o", default = ".", help = "location where map directory will be created")
    parser.add_argument("--layer", "-l", type = int, default = 0, help = "layer in Blender scene to load objects from (zero-indexed, default=0)")
    parser.add_argument("--actions", "-a", action = "store_true", help = "generate an extra boilerplate file for actions such as animating objects to edit it manually") 
    parser.add_argument("--no-spawns", action = "store_true", help = "don't include spawn points in map")

    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    args = parser.parse_args(argv)
    map_name = args.name
    out_dir = os.path.realpath(args.output)
    world_layer = args.layer
    generate_actions = args.actions
    generate_spawns = not args.no_spawns


    root_dir = os.path.join(out_dir, map_name)
    obj_dir = os.path.join(root_dir, "objects")
    if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
    if not os.path.isdir(obj_dir):
            os.makedirs(obj_dir)
    print("\n\nStarting to generate map file\n")

    object_list = []
    spawn_list = []
    for ob in bpy.data.objects:
        if ob.layers[world_layer]:
            if ob.type == "MESH":
                object_list.append(ob)
            elif ob.type == "EMPTY" and ob.name.startswith("spawn") and generate_spawns:
                spawn_list.append(ob)
    print("Found %d objects and %d spawnpoints\n" % (len(object_list), len(spawn_list)))
    
    filename = os.path.join(root_dir, map_name + ".nst")
    action_filename = os.path.join(root_dir, map_name + "_actions.nst")
    print("Writing to file %s" % filename)
    #open(filename, 'w').close() #to clear the contents of the file

    file = open(filename, 'w')
    file.write("<" + map_name + ">\n\n")
    write_objects(file, object_list)
    if generate_spawns:
        write_spawns(file, spawn_list)
    if generate_actions:
        write_action_boilerplate(action_filename, object_list)
    file.close()
    print("Done!")
    
if  __name__ =='__main__':
    main()
