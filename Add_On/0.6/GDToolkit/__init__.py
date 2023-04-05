bl_info = {
    "name" : "Leardo's Game Dev Toolkit",
    "author" : "Leardo",
    "version" : (0, 6),
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
    imp.reload(GDToolkit_FastVertexColorSet)
else:
    import bpy
    from . import GDToolkit_BatchExport
    from . import GDToolkit_MeshChecker
    from . import GDToolkit_FastVertexColorSet

        

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
            GDToolkit_MeshChecker.Select_Line,

            GDToolkit_FastVertexColorSet.GDToolkit_VColorSettings,
            GDToolkit_FastVertexColorSet.GDToolkit_VColorEdit,
            GDToolkit_FastVertexColorSet.GDToolkit_VColorEdit_Pie,
            GDToolkit_FastVertexColorSet.GDToolkit_VColorEdit_Enum,
           ]

addon_keymaps = []

def register():
    #print("register")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_renamesettings = bpy.props.PointerProperty(type=GDToolkit_BatchExport.RenameSettings) 
    bpy.types.Scene.ifEnable = bpy.props.BoolProperty(name="Enable Fast VC set",default=True) 
    

    kc = bpy.context.window_manager.keyconfigs.addon

    if kc:
        if 'Mesh' in kc.keymaps:
            km=kc.keymaps['Mesh']
        else:
            km = kc.keymaps.new(name='Mesh',space_type = 'VIEW_3D')

        kmi = km.keymap_items.new('gdtk.vcoloredit', 'Q', 'PRESS', alt=True)
        print(kmi) 
        addon_keymaps.append((km,kmi))

def unregister():
    #print("unregister")
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_renamesettings
    del bpy.types.Scene.ifEnable
    
    for km, kmi in addon_keymaps:
        print(km)
        print(kmi)
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
        