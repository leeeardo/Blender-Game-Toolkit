import bpy 
import os
     
class RenameSettings(bpy.types.PropertyGroup):
    prefix:bpy.props.StringProperty()
    suffix:bpy.props.StringProperty()
    suf_del_num:bpy.props.IntProperty()
    pre_del_num:bpy.props.IntProperty()
             
class MY_OT_OUTPUTBATCH(bpy.types.Panel):
    bl_label = "Batch Export FBX"
    bl_idname = "mytoolkit.OutputBatch"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Leardo's Toolkit"
    #bl_parent_id = "mytoolkit.gdtoolkit"

    
    def draw(self,context):
        layout = self.layout
        layout.operator("mytoolkit.batchexport_operator",icon="RENDER_STILL",text="Export Selected To Folder")
        
        layout.separator(factor=1)
        box = layout.box()
        row = box.row()
        
        
        renamesettings = context.scene.my_renamesettings
        row.prop(renamesettings,'prefix',text='Prefix')
        row.prop(renamesettings,'suffix',text = 'Suffix')              
        box.operator("mytoolkit.batchrename_operator",icon="FILE_TICK",text="Add Prefix&Suffix To Selected Objects")
        box = layout.box()
        #box.separator_spacer()
        row = box.row()
        
        row.prop(renamesettings,'pre_del_num',text='Pre Del Num')
        row.prop(renamesettings,'suf_del_num',text='Suf Del Num')
        box.operator("mytoolkit.batchremovename_operator",icon="FILE_TICK",text="Remove Pre&Suf of Selected Object's Name")
        
class BATCH_RENAME(bpy.types.Operator):
    bl_label = "Rename"
    bl_idname = "mytoolkit.batchrename_operator"
    
    def execute(self,context):
        selection = bpy.context.selected_objects
        renamesettings = context.scene.my_renamesettings
        for obj in selection:
            obj.name = renamesettings.prefix+obj.name+renamesettings.suffix
        return {"FINISHED"}

class BATCH_REMOVE_NAME(bpy.types.Operator):
    bl_label = "Remove name"
    bl_idname = "mytoolkit.batchremovename_operator"
    
    def execute(self,context):
        selection = bpy.context.selected_objects
        renamesettings = context.scene.my_renamesettings
        for obj in selection:
            obj.name = obj.name[renamesettings.pre_del_num:(len(obj.name)-renamesettings.suf_del_num)]
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
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx",use_selection = True)
            obj.select_set(False)
        
            #print("written",fn)
        
        view_layer.objects.active = obj_active
        for obj in selection:
            obj.select_set(True)
        
        return {"FINISHED"}
    
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)
    
