bl_info = {
	"name": "Tree",
	"author": "Kevin Caldwell",
	"version": (1, 0),
	"blender": (3, 00, 0),
	"location": "View3D > Add > Tree",
	"description": "Adds a new Tree Mesh Object",
	"warning": "",
	"doc_url": "",
	"category": "Tree",
}


import bpy
import random
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

x=0
y=1
z=2

max_iterations = 1

tree_vertices = [(0,0,0)]
tree_edges = []
decay_factor = 0.7

def get_tree_vertices(iterations = 0, vertex_list = [0,0,10]):
    if iterations != 0:
        global tree_vertices
        global tree_edges
        global decay_factor
        new_verts = []
        for i in range(len(vertex_list)):
            v = vertex_list[i]
            
            a = 1 / iterations + 0.1
            
            v1 = (v[x] + random.randint(-2, 2), v[y] + random.randint(-2, 2), v[z] + 10 * random.uniform(-1.0 + a, 1.0 + a) * decay_factor ** (max_iterations - iterations))
            v2 = (v[x] + random.randint(-2, 2), v[y] + random.randint(-2, 2), v[z] + 10 * random.uniform(-1.0 + a, 1.0 + a) * decay_factor ** (max_iterations - iterations))
            
            new_verts.append(v1)
            new_verts.append(v2)
            
            e1 = (len(tree_vertices) + i * 2, tree_vertices.index(v))
            e2 = (len(tree_vertices) + i * 2 + 1, tree_vertices.index(v))
            
            tree_edges.append(e1)
            tree_edges.append(e2)

        tree_vertices += new_verts
        get_tree_vertices(iterations - 1, new_verts)


def get_iteration(v = 0):
	for i in range(v):
		if 2 ** i > v:
			return i - 1
	return 1

	
def add_object(self, context):

	scale_x = self.scale.x
	scale_y = self.scale.y
	   
	global max_iterations
	global tree_vertices
	global tree_edges
	global decay_factor
	
	decay_factor = self.decay_factor
	
	random.seed(self.seed)
	   
	max_iterations = self.iterations
	tree_vertices = [(random.randint(-2,2),random.randint(-2,2),random.randint(4,7))]
	tree_edges = []
	
	mesh = bpy.data.meshes.new('Tree Mesh')
	get_tree_vertices(max_iterations, tree_vertices)
	
	tree_vertices.append((0,0,0))
	trunk = (0, len(tree_vertices) - 1)
	tree_edges.append(trunk)
	   
	mesh.from_pydata(tree_vertices, tree_edges, [])
	mesh.update()
	
	print(len(tree_vertices))
	object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
	"Create a new Tree Mesh Object"
	bl_idname = "mesh.add_tree"
	bl_label = "Generate New Tree"
	bl_options = {'REGISTER', 'UNDO'}
	
	scale: FloatVectorProperty(
		name="scale",
		default=(1.0, 1.0, 1.0),
		subtype='TRANSLATION',
		description="scaling",
	)
	   
	seed: bpy.props.IntProperty(
		name="Seed",
		default=0,
		subtype='NONE',
		description="pick seed",
	)
	
	iterations: bpy.props.IntProperty(
		name="Iterations",
		default=4,
		subtype='NONE',
		description="pick iterations",
	)
	
	decay_factor: bpy.props.FloatProperty(
		name="Decay Factor",
		default=0.7,
		subtype='NONE',
		description="pick iterations",
	)
	
	def execute(self, context):
	
		add_object(self, context)
		object = context.active_object
		skin = object.modifiers.new(name = "Skin", type = 'SKIN')
		skin.use_smooth_shade = True
		for i in range(len(object.data.skin_vertices[0].data) - 1):
			v = 0.3 / get_iteration(i)
			object.data.skin_vertices[0].data[i].radius = v, v
		object.modifiers.new(name = "Subdiv", type = 'SUBSURF')
		return {'FINISHED'}

# Registration

def add_object_button(self, context):
	self.layout.operator(
		OBJECT_OT_add_object.bl_idname,
		text="Tree",
		icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
	url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
	url_manual_mapping = (
		("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
	)
	return url_manual_prefix, url_manual_mapping


def register():
	bpy.utils.register_class(OBJECT_OT_add_object)
	bpy.utils.register_manual_map(add_object_manual_map)
	bpy.types.VIEW3D_MT_add.append(add_object_button)


def unregister():
	bpy.utils.unregister_class(OBJECT_OT_add_object)
	bpy.utils.unregister_manual_map(add_object_manual_map)
	bpy.types.VIEW3D_MT_add.remove(add_object_button)


if __name__ == "__main__":
	register()
