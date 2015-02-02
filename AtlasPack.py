from fbx import *
from PIL import Image

class Node:			
	x = property(fget=lambda self: self.area[0])
	y = property(fget=lambda self: self.area[1])
	x_edge = property(fget=lambda self: self.area[2])
	y_edge = property(fget=lambda self: self.area[3])
	width = property(fget=lambda self: self.x_edge - self.x)
	height = property(fget=lambda self: self.y_edge - self.y)

	def __init__(self, area):
		if len(area) == 2:
			area = (0,0,area[0],area[1])
		self.area = area
		pass

	def insert(self, area):
		# go down to child
		if hasattr(self, 'child'):
			a = self.child[0].insert(area)
			if a is None:
				a = self.child[1].insert(area)
			return a

		# is image fit to area
		image_area = Node(area)
		if image_area.width <= self.width and image_area.height <= self.height:
			self.child = [None, None]
			self.child[0] = Node((self.x + image_area.width, self.y,
								 self.x_edge, self.y + image_area.height))
			self.child[1] = Node((self.x, self.y + image_area.height,
								 self.x_edge, self.y_edge))

			return Node((self.x, self.y, self.x + image_area.width, self.y + image_area.height))

	pass # end of class Node

class Configure:
	def __init__(self):
		self.PACK_SIZE = [1024, 1024]
		self.nodes = {}
		self.Atlas = Image.new('RGBA', self.PACK_SIZE)


def Pack(configure):
	# initialize tree node
	tree = Node(configure.PACK_SIZE)

	print "[+] Start Packing"
	print "[--] Node count: ", len(configure.nodes)

	node_counter=1
	for node in configure.nodes.values():
		uv = tree.insert(node.image.size)
		if uv is None:
			# no child left
			raise ValueError("Pack Size too small.")

		
		configure.Atlas.paste(node.image, uv.area)

		layerElementUV = FbxLayerElementUV()

		# apply packed data to fbx uv
		if not node.uvSet.GetDirectArray() == None:
			node_counter+=1
			for vertexIndex in range(0, node.mesh.GetPolygonCount()*3):
				uv_point = node.uvSet.GetDirectArray().GetAt(vertexIndex)
				
				# apply to vertex uv data: y coordination is inverted
				x = uv_point[0] * float(uv.width)/float(configure.PACK_SIZE[0]) + float(uv.x)/float(configure.PACK_SIZE[0])
				y = 1 - (uv_point[1] * float(uv.height)/float(configure.PACK_SIZE[1]) + float(uv.y)/float(configure.PACK_SIZE[1]))

				node.uvSet.GetDirectArray().SetAt(vertexIndex, FbxVector2(x, y))


	return configure.Atlas


# main
if __name__=="__main__":
	# debug purpose
	import FBXTEST
	




