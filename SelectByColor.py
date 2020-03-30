bl_info = {
    "name": "Select face by color",
    "description": "Select all faces with same color on texture/UV.",
    "location": "(Edit Mode) Select > Select All by Trait",
    "author": "kodkuce",
    "blender": (2, 80, 0),
    "version": (0, 1),
    "category": "Mesh"
}

import bpy
import bmesh

def select_by_color():
    o = bpy.context.edit_object
    bm = bmesh.from_edit_mesh(o.data)
    uv_lay = bm.loops.layers.uv.active
    tx = o.active_material.node_tree.nodes["Image Texture"].image #get texture, should maybe check if connected to base color, but atm beh i know i have only 1 :)
    selected_color_uv = [ 0.0, 0.0, 0.0, 0.0 ]
    
    for f in bm.faces:
        if f.select: #for selected get uv position of first vert cuz we scale zero face anyway
            intX = int(round((tx.size[0]*f.loops[0][uv_lay].uv[0])))
            intY = int(round((tx.size[1]*f.loops[0][uv_lay].uv[1])))
    
            # go to texture img and extract its color so we can then select evry face that has same color (our goal)
            # target.Y * image width + target.X * 4 (as the table Pixels contains separate RGBA values)
            index = ( intY * tx.size[0] + intX ) * 4
            #print ("Field index: ", index)
    
            # aggregate the read pixel values into a nice array
            selected_color_uv = [
                tx.pixels[index], # RED
                tx.pixels[index + 1], # GREEN
                tx.pixels[index + 2], # BLUE
                tx.pixels[index + 3] # ALPHA
            ]
            #brake cuz we found selected no need to loop anymore
            break;
    
    #now we compere color to selected color and if same we select this face too
    for f in bm.faces:
        intX = int(round((tx.size[0]*f.loops[0][uv_lay].uv[0])))
        intY = int(round((tx.size[1]*f.loops[0][uv_lay].uv[1])))
        index = ( intY * tx.size[0] + intX ) * 4
    
        # aggregate the read pixel values into a nice array
        this_face_color = [
            tx.pixels[index], # RED
            tx.pixels[index + 1], # GREEN
            tx.pixels[index + 2], # BLUE
            tx.pixels[index + 3] # ALPHA
        ]
        
        if this_face_color == selected_color_uv :
            f.select = True
            
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    
class SelectFaces(bpy.types.Operator):
    """Select faces with same UV texture color"""
    bl_idname = 'face.select_same_c'
    bl_label = 'Select by color'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        select_by_color()
        return {'FINISHED'}

    def invoke(self, context, event) :
        select_by_color()
        return {"FINISHED"}
        


def menu_func(self, context):
    self.layout.operator(SelectFaces.bl_idname, text="Select by color")

def register():
   bpy.utils.register_class(SelectFaces)
   bpy.types.VIEW3D_MT_edit_mesh_select_by_trait.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SelectFaces)
    bpy.types.VIEW3D_MT_edit_mesh_select_by_trait.remove(menu_func)

if __name__ == "__main__":
    register()
