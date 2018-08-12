import bpy

class UI(bpy.types.Panel):
    bl_label = "MaterialNodeFinder"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    bpy.types.Scene.my_string = bpy.props.StringProperty(name='search for')
    bpy.types.Scene.my_list = []
    
    def draw(self,context):
        self.layout.prop(context.scene, "my_string")
        self.layout.operator("mnf.button")
        for l in bpy.types.Scene.my_list:
            self.layout.label(l[1],icon=l[0])
        
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
                        for gnod in mnod.node_tree.nodes:
                            if gnod.type == 'MATERIAL':
                                if  searchname in gnod.material.name:
                                    bpy.types.Scene.my_list.append(['MATERIAL_DATA',gnod.material.name + ' : ' + ' Grouped in '+ mnod.node_tree.name])
                            elif gnod.type == 'TEXTURE':
                                if searchname in gnod.texture.name:
                                    bpy.types.Scene.my_list.append(['TEXTURE',gnod.texture.name + ' : Grouped in ' + mnod.node_tree.name])
                        if searchname in mnod.node_tree.name:
                            bpy.types.Scene.my_list.append(['NODETREE',mnod.node_tree.name + ' : in ' + mat.name])
                    elif mnod.type == 'MATERIAL':
                        if searchname in mnod.material.name:
                            bpy.types.Scene.my_list.append(['MATERIAL_DATA',mnod.material.name + ' : in ' + mat.name])
                    elif mnod.type == 'TEXTURE':
                         if searchname in mnod.texture.name:
                            bpy.types.Scene.my_list.append(['TEXTURE',mnod.texture.name + ' : in ' + mat.name])
                            
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