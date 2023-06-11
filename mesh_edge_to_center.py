import bpy
import bmesh

# Check if the selected object is a mesh
if bpy.context.active_object.type == 'MESH':
    # Get the mesh data from the selected object
    obj = bpy.context.edit_object
    me = obj.data

    # Get the bmesh from the mesh data (Edit mode)
    bm = bmesh.from_edit_mesh(me)

    # Move each selected vertex to x=0
    for v in bm.verts:
        if v.select:
            v.co.x = 0

    # Update the bmesh and mesh data
    bmesh.update_edit_mesh(me)

else:
    print("Error: The selected object is not a mesh.")
