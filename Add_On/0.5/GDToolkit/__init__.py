bl_info = {
    "name" : "Leardo's Game Dev Toolkit",
    "author" : "Leardo",
    "version" : (0, 5),
    "blender" : (3, 1, 0),
    "location" : "View3D > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category": "View3D"
}
if "bpy" in locals():
    import imp
    imp.reload(GDToolkit_BatchExport)
    imp.reload(GDToolkit_MeshChecker)
else:
    import bpy
    from . import GDToolkit_BatchExport
    from . import GDToolkit_MeshChecker

        

classes = [
            GDToolkit_BatchExport.MY_OT_OUTPUTBATCH,
            GDToolkit_BatchExport.BATCH_EXPORT,
            GDToolkit_BatchExport.BATCH_RENAME,
            GDToolkit_BatchExport.BATCH_REMOVE_NAME,
            GDToolkit_BatchExport.RenameSettings,

            GDToolkit_MeshChecker.Mesh_Checker,
            GDToolkit_MeshChecker.Check_Selected_Obj,
            GDToolkit_MeshChecker.Set_Material,
            GDToolkit_MeshChecker.Select_Tris,
            GDToolkit_MeshChecker.Select_NGon,
            GDToolkit_MeshChecker.Select_Line
           ]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_renamesettings = bpy.props.PointerProperty(type=GDToolkit_BatchExport.RenameSettings)  
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_renamesettings


if __name__ == "__main__":
    register()
        