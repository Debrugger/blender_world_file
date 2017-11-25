import bpy

def main():
    for o in bpy.data.objects:
        o['type'] = 'platform'
        o['circular'] = True

if  __name__ =='__main__':
    main()
