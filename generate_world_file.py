#!/bin/python
import sys
import os
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description = "Generate an NST map data file from a scene in blender.")
    parser.add_argument("file", metavar = "FILENAME")
    parser.add_argument("--name", "-n", help = "name of the map", required = True)
    parser.add_argument("--output", "-o", default = ".", help = "location where map directory will be created")
    parser.add_argument("--layer", "-l", type = int, default = 0, help = "layer in Blender scene to load objects from (zero-indexed, default=0)")
    parser.add_argument("--actions", "-a", action = "store_true", help = "generate an extra boilerplate file for actions such as animating objects to edit it manually") 
    parser.add_argument("--no-spawns", action = "store_true", help = "don't include spawn points in map")
    args = parser.parse_args()

    pass_args = "--output %s --name %s --layer %d" % (args.output, args.name, args.layer)

    script_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "blender_export.py")

    command = ["blender", os.path.realpath(args.file), "--background", "--python", script_location, "--", "--output", args.output, "--name", args.name, "--layer", str(args.layer)]

    if args.actions:
        command.append("--actions")
    if args.no_spawns:
        command.append("--no-spawns")

    subprocess.call(command)

if __name__ == "__main__":
    main()
