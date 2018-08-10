import bpy

class UI(bpy.types.Panel):
    bl_label = "MaterialNodeFinder"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    bpy.types.Scene.my_string = bpy.props.StringProperty(name='string')
    bpy.types.Scene.my_list = []
    
    def draw(self,context):
        self.layout.prop(context.scene, "my_string")
        self.layout.operator("mnf.button")
        for l in bpy.types.Scene.my_list:
            self.layout.label(text='in '+l[1],icon=l[0])
        
class Button(bpy.types.Operator):
    bl_idname = "mnf.button"
    bl_label = "Find"

    def execute(self, context):

        bpy.types.Scene.my_list = []
        searchname = context.scene.my_string
        
        for mat in bpy.data.materials:
            if mat.use_nodes:
                for mnod in mat.node_tree.nodes:
                    if mnod.type == 'GROUP':
                        if mnod.node_tree.name == searchname:
                            bpy.types.Scene.my_list.append(['NODETREE',mat.name])
                    elif mnod.type == 'MATERIAL':
                        if mnod.material.name == searchname:
                            bpy.types.Scene.my_list.append(['MATERIAL_DATA',mat.name])
                    elif mnod.type == 'TEXTURE':
                         if mnod.texture.name == searchname:
                            bpy.types.Scene.my_list.append(['TEXTURE',mat.name])
                            
        return{'FINISHED'}
        
classes = (
    UI,
    Button
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        register_class(cls)

if __name__ == "__main__":
    register()