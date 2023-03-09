

import bpy
import bmesh
 
class CheckedObjData(bpy.types.PropertyGroup):
    tri_list=[]
    ngon_list=[]
    opline_list=[]


class Mesh_Checker(bpy.types.Panel):
    """Creates a Panel in view_3D side window"""
    bl_label = "Mesh Checker"
    bl_idname = "mytoolkit.meshchecker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Leardo's Toolkit"
    #bl_parent_id = "mytoolkit.gdtoolkit"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        #check
        row = layout.row()
        row.label(text='Tris num: '+str(len(context.scene.checkedobjdata.tri_list)))
        row.label(text='N-Gon num: '+str(len(context.scene.checkedobjdata.ngon_list)))
        row.label(text='OpenLine num: '+str(len(context.scene.checkedobjdata.opline_list)))
        layout.operator("mytoolkit.check_selected_obj")
        layout.operator("mytoolkit.set_materials")
        row = layout.row()
        row.operator('mytoolkit.select_tris')
        row.operator('mytoolkit.select_ngon')
        row.operator('mytoolkit.select_line')
        
class Check_Selected_Obj(bpy.types.Operator):
    bl_label="Check Selected Object"
    bl_idname = "mytoolkit.check_selected_obj"
    
    def execute(self,context):
        if bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        else:
            self.report({'ERROR'},"You Must Select One Object")
            return {"FINISHED"}
        
        obj = bpy.context.active_object
        print(obj.name)
        #deselect all
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        mesh = obj.data
        
        #set tris and N-Gon
        context.scene.checkedobjdata.tri_list.clear()
        context.scene.checkedobjdata.ngon_list.clear()
        context.scene.checkedobjdata.opline_list.clear()
        for face in mesh.polygons:
            if len(face.vertices) == 3:
                obj.data.polygons[face.index].select = True
                context.scene.checkedobjdata.tri_list.append(face.index)
            if len(face.vertices) > 4:
                obj.data.polygons[face.index].select = True
                context.scene.checkedobjdata.ngon_list.append(face.index)
    
        #find open line
        bm = bmesh.new()
        bm.from_mesh(mesh)
        edges = bm.edges[:]

        open_edges = [e for e in edges if len(e.link_faces) == 1]
        # Select the open edges
        context.scene.checkedobjdata.opline_list.clear()
        for e in open_edges:
            e.select_set(True)
            context.scene.checkedobjdata.opline_list.append(e.index)
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
        return {"FINISHED"}
    
    def CreateMats(self):
        for mat in bpy.data.materials:
            print(mat.name)
            if bpy.data.materials.find('_Tris') != -1:
                print("No NEED")
                return 
        print("NEED TO GEN")
        
        mat=bpy.data.materials.new(name="_Tris")
        mat.diffuse_color=(1,0,1,1)
        
        mat = bpy.data.materials.new(name="_N_GON")
        mat.diffuse_color=(1,0.2,0,1)
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
        
        # Assign the material to the object
        print(obj.data.materials)
        if len(obj.data.materials) ==0 :
            obj.data.materials.append( bpy.data.materials[bpy.data.materials.find('defaultMat')])
        
        # get mat in data
        trisMatIndex = bpy.data.materials.find('_Tris')
        trisMat = bpy.data.materials[trisMatIndex]
        nGonMatIndex = bpy.data.materials.find('_N_GON')
        nGonMat = bpy.data.materials[nGonMatIndex]
    
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
        for tri in context.scene.checkedobjdata.tri_list:
            bm.faces.ensure_lookup_table()
            bm.faces[tri].material_index = trisMatIndex
        for ngon in context.scene.checkedobjdata.ngon_list:
            bm.faces.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            bm.faces[ngon].material_index = nGonMatIndex
            
        bm.free()
 

class Select_Tris(bpy.types.Operator):
    bl_label="Select Triangle"
    bl_idname = "mytoolkit.select_tris" 
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        
        obj = bpy.context.active_object
        
        for tri in context.scene.checkedobjdata.tri_list:
             obj.data.polygons[tri].select = True
            
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        return {'FINISHED'}
  

class Select_NGon(bpy.types.Operator):
    bl_label="Select N-Gon"
    bl_idname = "mytoolkit.select_ngon" 
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        
        obj = bpy.context.active_object
        
        for ngon in context.scene.checkedobjdata.ngon_list:
             obj.data.polygons[ngon].select = True
            
        
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
        
        for opline in context.scene.checkedobjdata.opline_list:
            edges[opline].select_set(True)
            
        
        # Free the BMesh object
        bm.to_mesh(bpy.context.active_object.data)
        bm.free()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="EDGE")
        return {'FINISHED'}
         