bl_info = {
    "name" : "My Toolkit_MeshChecker",
    "author" : "Leardo",
    "version" : (1, 0),
    "blender" : (3, 1, 0),
    "location" : "View3D > Tool",
    "warning" : "",
    "wiki_url" : "",
}

import bpy
import bmesh

class CheckTriIntData(bpy.types.PropertyGroup):
    tri_index: bpy.props.IntProperty(name="tri index",default=0)
    #ngon_index: bpy.props.IntProperty(name="ngon index",default=0)
class CheckNGonIntData(bpy.types.PropertyGroup):
    NGon_index: bpy.props.IntProperty(name="Ngon index",default=0)
class CheckOpenLinenIntData(bpy.types.PropertyGroup):
    openline_index: bpy.props.IntProperty(name="OpenLine index",default=0)   
    
    
class CheckedObjData(bpy.types.PropertyGroup):
    tri_num:bpy.props.IntProperty(name="triangles number",default=0)
    NGon_num:bpy.props.IntProperty(name="N-Gon number")
    openLine_num:bpy.props.IntProperty(name="OpenLine number")


class Mesh_Checker(bpy.types.Panel):
    """Creates a Panel in view_3D side window"""
    bl_label = "Mesh Checker"
    bl_idname = "mytoolkit.meshchecker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Leardo's Toolkit"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        #check
        row = layout.row()
        row.label(text='Tris num: '+str(context.scene.checkedobjdata.tri_num))
        row.label(text='N-Gon num: '+str(context.scene.checkedobjdata.NGon_num))
        row.label(text='OpenLine num: '+str(context.scene.checkedobjdata.openLine_num))
        layout.operator("mytoolkit.check_selected_obj")
        layout.operator("mytoolkit.set_materials")
        row = layout.row()
        row.operator('mytoolkit.select_tris')
        row.operator('mytoolkit.select_ngon')
        row.operator('mytoolkit.select_line')
        #display
        
        
        #set viewportdisplay
class Check_Selected_Obj(bpy.types.Operator):
    bl_label="Check Selected Object"
    bl_idname = "mytoolkit.check_selected_obj"
    
    def execute(self,context):
        
        obj = bpy.context.active_object
        
        #deselect all
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        mesh = obj.data
        
        #set tris and N-Gon
        context.scene.checkedobjdata.tri_num=0
        context.scene.checktriintdata.clear()
        context.scene.checkedobjdata.NGon_num=0
        context.scene.checkNGonintdata.clear()
        for face in mesh.polygons:
            if len(face.vertices) == 3:
                obj.data.polygons[face.index].select = True
                context.scene.checkedobjdata.tri_num+=1
                #print(face.index)
                context.scene.checktriintdata.add().tri_index=face.index
            if len(face.vertices) > 4:
                obj.data.polygons[face.index].select = True
                context.scene.checkedobjdata.NGon_num+=1
                #print(face.index)
                context.scene.checkNGonintdata.add().NGon_index=face.index
                #print(face.index)
    
        #find open line
        bm = bmesh.new()
        bm.from_mesh(mesh)
        edges = bm.edges[:]

        open_edges = [e for e in edges if len(e.link_faces) == 1]
        # Select the open edges
        context.scene.checkedobjdata.openLine_num=0
        context.scene.checkopenlineintdata.clear()
        #context.scene.checkNGonintdata.clear()
        for e in open_edges:
            e.select_set(True)
            context.scene.checkedobjdata.openLine_num+=1
            context.scene.checkopenlineintdata.add().openline_index=e.index
            print(e.index)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Free the BMesh object
        bm.to_mesh(mesh)
        bm.free()
    
    
        bpy.ops.object.mode_set(mode = 'EDIT')
        return {"FINISHED"}         
    
    

class Set_Material(bpy.types.Operator):
    bl_label="Enable/Disable Material"
    bl_idname = "mytoolkit.set_materials" 
    
    def execute(self,context):
        self.CreateMats()
        self.SetMats(context)
        #bpy.ops.object.select_all(action='DESELECT')
        return {"FINISHED"}
    
    def CreateMats(self):
        #print(len(bpy.data.materials))
        for mat in bpy.data.materials:
            print(mat.name)
            if bpy.data.materials.find('_Tris') != -1:
                print("No NEED")
                return 
        print("NEED TO GEN")
        
        mat=bpy.data.materials.new(name="_Tris")
        mat.diffuse_color=(1,0,0,1)
        
        mat = bpy.data.materials.new(name="_N_GON")
        mat.diffuse_color=(1,1,0,1)
        bpy.data.materials.new(name="defaultMat")
    
    def SetMats(self,context):
        obj = bpy.context.active_object
        
        #if disable
        if obj.data.materials.find('_Tris') !=-1:
            if obj.mode == 'EDIT':
                bpy.ops.object.mode_set(mode = 'OBJECT') 
            
            trisMatIndex = obj.data.materials.find('_Tris')
            nGonMatIndex = obj.data.materials.find('_N_GON')
            
            obj.active_material_index = trisMatIndex
            bpy.ops.object.material_slot_remove()
            obj.active_material_index = nGonMatIndex
            bpy.ops.object.material_slot_remove()
            return
        
        
        #if sel obj has no material
        # Get the active object
        
        # Assign the material to the object
        if obj.data.materials is None:
            obj.data.materials[0] =  bpy.data.materials[bpy.data.materials.find('defaultMat')]
        #else:
        #    obj.data.materials.append( bpy.data.materials[bpy.data.materials.find('defaultMat')])
        
        # get mat in data
        trisMatIndex = bpy.data.materials.find('_Tris')
        trisMat = bpy.data.materials[trisMatIndex]
        nGonMatIndex = bpy.data.materials.find('_N_GON')
        nGonMat = bpy.data.materials[nGonMatIndex]
        #obj = context.active_object
        #print(len(obj.data.materials))
    
        #append mat
        obj.data.materials.append(trisMat)
        obj.data.materials.append(nGonMat)
        trisMatIndex = obj.data.materials.find('_Tris')
        nGonMatIndex = obj.data.materials.find('_N_GON')
        #set mat assign
        mesh = obj.data
        
        
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode = 'EDIT') 
        bm = bmesh.from_edit_mesh(mesh)
        for data in context.scene.checktriintdata:
            bm.faces.ensure_lookup_table()
            bm.faces[data.tri_index].material_index = trisMatIndex
        for data in context.scene.checkNGonintdata:
            print(bm.faces[data.NGon_index].material_index)
            bm.faces.ensure_lookup_table()
            bm.faces[data.NGon_index].material_index = nGonMatIndex
            #bm.faces[data.NGon_index].select = False
            print(bm.faces[data.NGon_index].material_index)
 

class Select_Tris(bpy.types.Operator):
    bl_label="Select Triangle"
    bl_idname = "mytoolkit.select_tris" 
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'EDIT') 
        #bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        
        obj = bpy.context.active_object
        
        #obj.data.polygons[face.index].select = True
        
        for data in context.scene.checktriintdata:
             obj.data.polygons[data.tri_index].select = True
            
        
        # Free the BMesh object
    
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        return {'FINISHED'}
  

class Select_NGon(bpy.types.Operator):
    bl_label="Select N-Gon"
    bl_idname = "mytoolkit.select_ngon" 
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'EDIT') 
        #bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        
        obj = bpy.context.active_object
        
        #obj.data.polygons[face.index].select = True
        
        for data in context.scene.checkNGonintdata:
             obj.data.polygons[data.NGon_index].select = True
            
        
        # Free the BMesh object
    
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        return {'FINISHED'}  
    
    
class Select_Line(bpy.types.Operator):
    bl_label="Select OpenLine"
    bl_idname = "mytoolkit.select_line" 
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'EDIT') 
        #bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bm = bmesh.new()
        bm.from_mesh(bpy.context.active_object.data)
        edges = bm.edges[:]
        
        #edges = bpy.context.active_object.data.edges
        for data in context.scene.checkopenlineintdata:
            edges[data.openline_index].select_set(True)
            
        
        # Free the BMesh object
        bm.to_mesh(bpy.context.active_object.data)
        bm.free()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="EDGE")
        return {'FINISHED'}
         


classes = [
            Mesh_Checker,
            Check_Selected_Obj,
            CheckTriIntData,
            CheckNGonIntData,
            CheckedObjData,
            CheckOpenLinenIntData,
            Set_Material,
            Select_Tris,
            Select_NGon,
            Select_Line
            ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.utils.register_class(CheckedObjData)
    bpy.types.Scene.checkedobjdata = bpy.props.PointerProperty(type=CheckedObjData)
    bpy.types.Scene.checktriintdata=bpy.props.CollectionProperty(type=CheckTriIntData)
    bpy.types.Scene.checkNGonintdata=bpy.props.CollectionProperty(type=CheckNGonIntData)
    bpy.types.Scene.checkopenlineintdata=bpy.props.CollectionProperty(type=CheckOpenLinenIntData)
    #checkedobjdata.tri_face=bpy.props.CollectionProperty(type=bpy.types.MeshPolygon)
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.checkedobjdata
    del bpy.types.Scene.checkintdata

if __name__ == "__main__":
    register()
