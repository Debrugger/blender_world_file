import sys
import os
import argparse
import bpy
import shutil
import subprocess
from PIL import Image
import imghdr

def write_objects(f, objects, tex_dir, convert_textures):
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

        try:
            diff_path = os.path.realpath(bpy.path.abspath(i.material_slots[0].material.texture_slots[0].texture.image.filepath_raw))
        except:
            diff_path = ""
        #try:
        #    spec_path = os.path.realpath(bpy.path.abspath(i.material_slots[0].material.texture_slots[1].texture.image.filepath_raw))
        #except:
        #    spec_path = ""
        #try:
        #    nrm_path = os.path.realpath(bpy.path.abspath(i.material_slots[0].material.texture_slots[2].texture.image.filepath_raw))
        #except:
        #    nrm_path = ""

        #try:
        if diff_path != "":
            handle_image(diff_path, tex_dir, "tex_diff", convert_textures, f)
        #except:
        #    print("Could not copy file from %s to %s" % (diff_path, tex_dir))
        
        #try:
        #    handle_image(spec_path, tex_dir, "tex_spec", convert_textures, f)
        #except:
        #    print("Could not copy file from %s to %s" % (spec_path, tex_dir))
        #
        #try:
        #    handle_image(nrm_path, tex_dir, "tex_nrm", convert_textures, f)
        #except:
        #    print("Could not copy file from %s to %s" % (nrm_path, tex_dir))

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

def export_objects(objects, dir):
    lookup = {}     #only export every mesh once, if we already exported it skip
    for o in objects:
        o.select = False
    for o in objects:
        if not o.data.name in lookup.values():
            lookup[o.data.name] = True
            o.select = True
            bpy.ops.export_scene.obj(filepath = os.path.join(dir,  o.data.name) + ".obj", use_selection = True, use_materials = False)
            o.select = False

def handle_image(src_path, dst_path, tex_name, convert, file):
    img_name = os.path.splitext(os.path.basename(src_path))[0]
    ext = os.path.splitext(os.path.basename(src_path))[1]
    if convert and imghdr.what(src_path) != "png":
        w, h = Image.open(src_path).size
        command = ["convert", src_path]
        if w * h > 1024 * 1024:
            command.append("-resize")
            command.append("1024x")
        command.append(os.path.join(dst_path, img_name + ".png"))
        subprocess.call(command)
    else:
        print("Copying %s to %s" % (src_path, dst_path))
        shutil.copy2(src_path, dst_path)
    file.write(tex_name + "=" + os.path.basename(src_path) + "\n" if convert else (img_name + ".png\n"))


#create directories for map
def main():
    parser = argparse.ArgumentParser(description = "Generate an NST map data file from a scene in blender. This program is made to be executed from the Blender python environment.")
    parser.add_argument("--name", "-n", help = "name of the map", required = True)
    parser.add_argument("--output", "-o", default = ".", help = "location where map directory will be created")
    parser.add_argument("--layer", "-l", type = int, default = 0, help = "layer in Blender scene to load objects from (zero-indexed, default=0)")
    parser.add_argument("--actions", "-a", action = "store_true", help = "generate an extra boilerplate file for actions such as animating objects to edit it manually") 
    parser.add_argument("--no-spawns", action = "store_true", help = "don't include spawn points in map")
    parser.add_argument("--convert-textures", "-c", action = "store_true", help = "convert all textures to PNG")

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
    tex_dir = os.path.join(root_dir, "textures")
    if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
    if not os.path.isdir(obj_dir):
            os.makedirs(obj_dir)
    if not os.path.isdir(tex_dir):
            os.makedirs(tex_dir)
    print("\n\nStarting to generate map file\n")

    object_list = []
    spawn_list = []
    for ob in bpy.data.objects:
        if ob.layers[world_layer]:
            if ob.type == "MESH":
                object_list.append(ob)
            elif ob.type == "EMPTY" and ob.name.startswith("spawn") and generate_spawns:
                spawn_list.append(ob)
    print("\nFound %d objects and %d spawnpoints\n" % (len(object_list), len(spawn_list)))
    
    filename = os.path.join(root_dir, map_name + ".nst")
    action_filename = os.path.join(root_dir, map_name + "_actions.nst")
    action_file_exists = False
    if os.path.isfile(action_filename):
        print("Action file already exists, it will not be overwritten.")
        action_file_exists = True
    #open(filename, 'w').close() #to clear the contents of the file

    export_objects(object_list, obj_dir)

    file = open(filename, 'w')
    file.write("<" + map_name + ">\n\n")
    write_objects(file, object_list, tex_dir, args.convert_textures)
    if generate_spawns:
        write_spawns(file, spawn_list)
    if generate_actions and not action_file_exists:
        write_action_boilerplate(action_filename, object_list)
    file.close()
    print("Done!")
    
if  __name__ =='__main__':
    main()
