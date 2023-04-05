import bpy
from bpy.types import Menu
import random
import bmesh


class GDToolkit_VColorSettings(bpy.types.Panel):
    bl_label = "Fast Vertex Color"
    bl_idname = "mytoolkit.vcolorsettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Leardo's Toolkit"
    

    def draw(self, context):
        layout = self.layout
        #op = layout.operator("gdtk.vcoloredit")
        layout.prop(context.scene, "ifEnable", 
            text="Enable Ops",
            icon='CHECKBOX_HLT' if context.scene.ifEnable else 'CHECKBOX_DEHLT' )

class GDToolkit_VColorEdit(bpy.types.Operator):
    bl_idname = "gdtk.vcoloredit"
    bl_label = "VertexColor Fast Edit"
    bl_options = {'REGISTER', 'UNDO'}

    #enableOps:bpy.props.BoolProperty(default=True)
    def execute(self, context):
        if context.scene.ifEnable:
            bpy.ops.wm.call_menu_pie(name="gdtoolkit.vcoloreditpie")
        return {'FINISHED'}

class GDToolkit_VColorEdit_Pie(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Fast VertexColor Ops"
    bl_idname = "gdtoolkit.vcoloreditpie"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        pie.operator_enum("gdtk.vceditenum", "mode")

from bpy.props import EnumProperty
from bpy.types import Operator

class GDToolkit_VColorEdit_Enum(Operator):
    bl_idname = "gdtk.vceditenum"
    bl_label = "Enum"

    mode: EnumProperty(
        items=[
            ('OPTION1', "Assign Random Color", "The first option"),
            ('OPTION2', "Assign To Seam Faces", "The second option"),
            ('OPTION3', "Switch Color Type", "The third option"),
        ],
        name="Mode",
        default='OPTION1'
    )

    def initIDGroup(self,context):
        ca_name = "ID map"
        obj=bpy.context.active_object
        
        if bpy.app.version[1]>=2:
            attributes = obj.data.color_attributes
            #print(attributes.active_color_index)
            if not attributes.get(ca_name):
                attributes.new(ca_name,"BYTE_COLOR","CORNER")
            idAttribute = attributes.get(ca_name)
            #index=-1
            attributes.active_color = idAttribute
            attributes.render_color_index = attributes.active_color_index
            #vertex_colors[index].active_render=True
            #print(obj.data.attributes)
            #obj.data.attributes.active_color_index=index
            #print(attributes.active_color_index)
            ver=bpy.app.version
            #print(ver[1])
            return attributes.active_color_index
        else:
            obj=bpy.context.active_object
            vertex_colors = obj.data.vertex_colors
            index=-1
            for i in range(len(vertex_colors)):
                if vertex_colors[i].name =="ID map":
                    index=i
                    break
            if index==-1:
                vertex_colors.new(name="ID map")
                index=len(vertex_colors)-1
            vertex_colors[index].active_render=True
            vertex_colors.active_index=index
            #print(dir(vertex_colors))
            return index

    def execute(self, context):
        if self.mode == 'OPTION1':
            index = self.initIDGroup(context)
            #index=0
            #print(index)
            obj=bpy.context.active_object
            vertex_colors = obj.data.vertex_colors
            
            color = [random.random(),random.random(),random.random(),1.0]
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            bm = bmesh.from_edit_mesh(obj.data)
            selected_faces = [f for f in bm.faces if f.select]
            
            vertex_colors = bm.loops.layers.color.active
            for face in selected_faces:
                for loop in face.loops:
                    loop[vertex_colors] = color
            bmesh.update_edit_mesh(obj.data)
            
        elif self.mode == 'OPTION2':
            index = self.initIDGroup(context)
            #print(index)
            obj=bpy.context.active_object
            vertex_colors = obj.data.vertex_colors
            bpy.ops.mesh.select_linked(delimit={'SEAM'})
            color = [random.random(),random.random(),random.random(),1.0]
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            bm = bmesh.from_edit_mesh(obj.data)
            selected_faces = [f for f in bm.faces if f.select]
            
            vertex_colors = bm.loops.layers.color.active
            for face in selected_faces:
                for loop in face.loops:
                    loop[vertex_colors] = color
            bmesh.update_edit_mesh(obj.data)
        elif self.mode == 'OPTION3':
            if bpy.context.space_data.shading.color_type == 'MATERIAL':
                bpy.context.space_data.shading.color_type = 'VERTEX'
            else:
                bpy.context.space_data.shading.color_type = 'MATERIAL'

        #print("Selected mode:", self.mode)
        return {'FINISHED'}


