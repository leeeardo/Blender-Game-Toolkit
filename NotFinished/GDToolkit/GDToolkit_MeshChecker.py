

import bpy
import bmesh
 

#enableMat = False  
testDic = {}

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

        layout.operator("mytoolkit.check_selected_obj")
        layout.operator("mytoolkit.set_materials")
        row = layout.row()
        row.operator('mytoolkit.select_tris')
        row.operator('mytoolkit.select_ngon')
        row.operator('mytoolkit.select_line')
        #check
        box = layout.box()
        box.column_flow(columns=2, align=False)
        for k,v in testDic.items():
            #print(k,":",v)
            row = box.row()
            row.label(text=k+':')
            row.label(text='Tris:'+str(len(v[0])))
            row.label(text='N-Gon:'+str(len(v[1])))
            row.label(text='OpenLine:'+str(len(v[2])))
        
class Check_Selected_Obj(bpy.types.Operator):
    bl_label="Check Selected Object"
    bl_idname = "mytoolkit.check_selected_obj"
    
    def execute(self,context):
        if bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        else:
            #self.report({'ERROR'},"You Must Select One Object")
            testDic.clear()
            return {"FINISHED"}
        
        #obj = bpy.context.active_object
        selection = bpy.context.selected_objects
        #print(obj.name)
        #deselect all
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

       # 
        
        #set tris and N-Gon
        
        testDic.clear()
        
        for obj in selection:
            mesh = obj.data
            name = obj.name
            trilist=[]
            ngonlist=[]
            oplinelist=[]
            
            for face in mesh.polygons:
                if len(face.vertices) == 3:
                    obj.data.polygons[face.index].select = True
                    trilist.append(face.index)
                if len(face.vertices) > 4:
                    obj.data.polygons[face.index].select = True
                    ngonlist.append(face.index)
                    
            #find open line
            bm = bmesh.new()
            bm.from_mesh(mesh)
            edges = bm.edges[:]

            open_edges = [e for e in edges if len(e.link_faces) == 1]
            # Select the open edges
            
            for e in open_edges:
                e.select_set(True)
                
                oplinelist.append(e.index)
                
            testDic[name]=[trilist,ngonlist,oplinelist,0]
        
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            bpy.ops.object.mode_set(mode='OBJECT')

            # Free the BMesh object
            bm.to_mesh(mesh)
            bm.free()
            
            for k,v in testDic.items():
                print(k,":",v)

        #bpy.ops.object.mode_set(mode = 'EDIT')
        return {"FINISHED"}         
    
    
#isMatting = False
class Set_Material(bpy.types.Operator):
    bl_label="Enable/Disable Material"
    bl_idname = "mytoolkit.set_materials" 
    
    
    def execute(self,context):
        global isMatting
        self.CreateMats()
        self.SetMats(context)
        #isMatting = not isMatting
        
        
        return {"FINISHED"}
    
    def CreateMats(self):
        for mat in bpy.data.materials:
            print(mat.name)
            if bpy.data.materials.find('_Tris') != -1:
                #print("No NEED")
                return 
        print("NEED TO GEN")
        
        mat=bpy.data.materials.new(name="_Tris")
        mat.diffuse_color=(1,0,1,1)
        
        mat = bpy.data.materials.new(name="_N_GON")
        mat.diffuse_color=(1,0.2,0,1)
        bpy.data.materials.new(name="defaultMat")
    
    def SetMats(self,context):
        
        selection = bpy.context.selected_objects
        #global isMatting
        #print(isSetMat)
         #if disable
        
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        #bpy.ops.object.select_all(action='DESELECT')
        for obj in selection:
            if testDic[obj.name][3] == 1:
                bpy.context.view_layer.objects.active = obj
                trisMatIndex = obj.data.materials.find('_Tris')
                nGonMatIndex = obj.data.materials.find('_N_GON')
                obj.active_material_index = trisMatIndex
                bpy.ops.object.material_slot_remove()
                obj.active_material_index = nGonMatIndex
                bpy.ops.object.material_slot_remove()
            else:
                if len(obj.data.materials) ==0 :
                    obj.data.materials.append(bpy.data.materials[bpy.data.materials.find('defaultMat')])
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
                bm.faces.ensure_lookup_table()
                for tri in testDic[obj.name][0]:
                    bm.faces[tri].material_index = trisMatIndex
                for ngon in testDic[obj.name][1]:
                    bm.faces[ngon].material_index = nGonMatIndex
                bpy.ops.object.mode_set(mode = 'OBJECT')
            testDic[obj.name][3] = int(not bool(testDic[obj.name][3]))
            #testDic[obj.name][3] = int(not bool(testDic[obj.name][3]))
                
            #isSetMat = False
        
        
            # Assign the material to the object
            
                #bm.free()
            #isSetMat = True
        #isSetMat = not isSetMat
        #print(isSetMat)
 
class Select_Tris(bpy.types.Operator):
    bl_label="Select Triangle"
    bl_idname = "mytoolkit.select_tris" 
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        
        #obj = bpy.context.active_object
        selection = bpy.context.selected_objects
        
        for obj in selection:
            for tri in testDic[obj.name][0]:
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
        
        #obj = bpy.context.active_object
        selection = bpy.context.selected_objects
        
        for obj in selection:
            for ngon in testDic[obj.name][1]:
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
        
        
        selection = bpy.context.selected_objects
        
        for obj in selection:
            bpy.context.view_layer.objects.active = obj
            bm = bmesh.new()
            bm.from_mesh(bpy.context.active_object.data)
            edges = bm.edges[:]
            for opline in testDic[obj.name][2]:
                edges[opline].select_set(True)
            bm.to_mesh(bpy.context.active_object.data)
            bm.free()
        
        # Free the BMesh object
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="EDGE")
        return {'FINISHED'}


# classes = [
#             Mesh_Checker,
#             Check_Selected_Obj,
#             Set_Material,
#             Select_Tris,
#             Select_NGon,
#             Select_Line,
#            ]
# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)
    
# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)

# if __name__ == "__main__":
#     register()
         