bl_info = {
    "name" : "My Toolkit_BatchExport",
    "author" : "Leardo",
    "version" : (1, 0),
    "blender" : (3, 1, 0),
    "location" : "View3D > Tool",
    "warning" : "",
    "wiki_url" : "",
}

import bpy 
import os
     
     
sufix = [
    ("HP","High Poly",""),
    ("LP","Low Poly",""),
]
     
class RenameSettings(bpy.types.PropertyGroup):
    render_type:bpy.props.EnumProperty(items=[
        ("FBX",".fbx",""),
        ("OBJ",".obj",""),
        ])
    rename_type:bpy.props.EnumProperty(items=sufix)
     
             
class MY_OT_OUTPUTBATCH(bpy.types.Panel):
    bl_label = "Batch Operator"
    bl_idname = "mytoolkit.OutputBatch"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Leardo's Toolkit"

    
    def draw(self,context):
        my_renamesettings = context.scene.my_renamesettings
        
        layout = self.layout
        row = layout.row()
        row.prop(my_renamesettings,"render_type",text = "")
        row.operator("mytoolkit.batchexport_operator",icon="RENDER_STILL",text="Export To Folder")
        
        
        layout.separator(factor=2)
        row = layout.row()
        
        layout.prop(my_renamesettings,"rename_type",text = "rename type")
        layout.operator("mytoolkit.batchrename_operator",icon="FILE_TICK",text="Rename Selected Object")
        
class BATCH_RENAME(bpy.types.Operator):
    bl_label = "Rename"
    bl_idname = "mytoolkit.batchrename_operator"
    
    def execute(self,context):
        selection = bpy.context.selected_objects
        
        if not selection:
            raise Exception("Please Select Objects")
        
        for obj in selection:
            if context.scene.my_renamesettings.rename_type == "HP":
                if not obj.name.endswith('_HP'):
                    obj.name = obj.name+"_HP"
            if context.scene.my_renamesettings.rename_type == "LP":
                if not obj.name.endswith('_LP'):
                    obj.name = obj.name+"_LP"

        return {"FINISHED"}
        
        
class BATCH_EXPORT(bpy.types.Operator):
    bl_label = "Export"
    bl_idname = "mytoolkit.batchexport_operator"
    
    path : bpy.props.StringProperty(name="File Name",default="")
    
    def execute(self, context):
        p = self.path
        
        basedir = os.path.dirname(bpy.data.filepath)
        
        if not basedir:
            raise Exception("Blend file is not saved")
        
         #create folder
        folderpath = basedir+"\\"+p+"\\"
        folder = os.path.exists(folderpath)
        if folder==False:
            os.makedirs(folderpath)
        
        view_layer = bpy.context.view_layer
        
        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in selection:
            obj.select_set(True)
            
            collection = obj.users_collection[0]
           
            view_layer.objects.active = obj
            
            name = bpy.path.clean_name(obj.name)
            name = collection.name+"_"+name
            fn = os.path.join(folderpath,name)
            if bpy.context.scene.my_renamesettings.render_type == 'FBX':
                bpy.ops.export_scene.fbx(filepath=fn + ".fbx",use_selection = True)
            if bpy.context.scene.my_renamesettings.render_type == 'OBJ':
                bpy.ops.export_scene.obj(filepath=fn + ".obj",use_selection = True)
            obj.select_set(False)
        
            #print("written",fn)
        
        view_layer.objects.active = obj_active
        for obj in selection:
            obj.select_set(True)
        
        return {"FINISHED"}
    
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)
        
def register():
    bpy.utils.register_class(MY_OT_OUTPUTBATCH)
    bpy.utils.register_class(BATCH_EXPORT)
    bpy.utils.register_class(BATCH_RENAME)
    
    bpy.utils.register_class(RenameSettings)
    bpy.types.Scene.my_renamesettings = bpy.props.PointerProperty(type=RenameSettings)
    
def unregister():
    bpy.utils.unregister_class(MY_OT_OUTPUTBATCH)
    bpy.utils.unregister_class(BATCH_EXPORT)
    bpy.utils.unregister_class(BATCH_RENAME)
    
if __name__ == "__main__":
    register()