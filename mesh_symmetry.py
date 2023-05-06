import bpy
import bmesh
import mathutils

def find_closest_vert(verts, target_co):
    closest_vert = None
    min_distance = float('inf')
    for v in verts:
        distance = (v.co - mathutils.Vector(target_co)).length
        if distance < min_distance:
            min_distance = distance
            closest_vert = v
    return closest_vert

# Check if the selected object is a mesh
if bpy.context.active_object.type == 'MESH':
    # Get the mesh data from the selected object
    obj = bpy.context.edit_object
    me = obj.data

    # Create a bmesh object from the mesh data
    bm = bmesh.new()
    bm.from_mesh(me)

    # Move each selected vertex to x=0
    selected_verts = [v for v in bm.verts if v.select]
    bmesh.ops.translate(bm, vec=(-selected_verts[0].co.x, 0, 0), verts=selected_verts)

    # Get the left and right side vertices
    left_verts = []
    right_verts = []
    for v in bm.verts:
        if not v.select:
            if v.co.x < 0:
                left_verts.append(v)
            elif v.co.x > 0:
                right_verts.append(v)

    # Move each vertex on the left side to snap symmetrically to the right side
    for left_vert in left_verts:
        mirrored_vert = left_vert.co.copy()
        mirrored_vert.x = -mirrored_vert.x
        closest_right_vert = find_closest_vert(right_verts, mirrored_vert)
        if closest_right_vert:
            left_vert.co = closest_right_vert.co.copy()
            left_vert.co.x = -left_vert.co.x

    # Clear all sharp edges
    for e in bm.edges:
        e.smooth = True

    # Update the mesh data from the bmesh object
    bpy.ops.object.mode_set(mode='OBJECT')
    bm.to_mesh(me)
    bm.free()

    # Update the mesh in the viewport
    bpy.ops.object.mode_set(mode='EDIT')

else:
    print("Error: The selected object is not a mesh.")
