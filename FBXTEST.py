# -*- coding: utf-8 -*-

"""""""""""""""""""""""""""""""""""""""""""""
#############################################

          Author: minu jeong

          Dependency: FbxSdk, PIL

          Written: 2015. 1

#############################################
"""""""""""""""""""""""""""""""""""""""""""""


from fbx import *
from PIL import Image, ImageColor
import sys, glob, time, os
import random, math
import FbxCommon
import AtlasPack, UVSetNamer


sizes = ([128, 128], [64, 64])
background_colors = ((30, 20, 30), (50, 30, 30), (30, 50, 30), (30, 30, 50), (10, 30, 50), (40, 30, 40))
dirname = "results"
uvs = []
configure = AtlasPack.Configure()
managers_and_scenes_and_filenames = []

class MeshUVNode(object):
	def __init__(self, mesh, uvSet, image):
		self.mesh = mesh
		self.uvSet = uvSet
		self.image = image

	def __repr__(self):
		return "Polycount: %d, Image: " % self.mesh.GetPolygonCount() + str(self.image)


# Get Mesh
def GetMeshFromScene(scene):
	meshes = []
	for i in range(0, scene.GetNodeCount()):
		node = scene.GetNode(i)
		mesh = node.GetMesh()
		if not None == mesh:
			meshes.append(mesh)
	return meshes

# Get UV
def GetUVSetFromMesh(mesh):
	uvs_from_mesh = []
	
	uvSetNameList = [""]
	mesh.GetUVSetNames(uvSetNameList)
	
	for index in range(0, len(uvSetNameList)):
		layerElementUV = mesh.GetElementUV(index)
		if not None == layerElementUV:
			if "" == uvSetNameList[index]:
				uvSetNameList[index] = UVSetNamer.Name()
			uvs_from_mesh.append((uvSetNameList[index], layerElementUV))

	# returns [name, uv_element]
	return uvs_from_mesh
	

def packScene(fbxFile):
	print "Packing file: %s"%(fbxFile)

	# init
	sm, sc = FbxCommon.InitializeSdkObjects()
	managers_and_scenes_and_filenames.append((sm, sc, fbxFile))

	# loads scene
	FbxCommon.LoadScene(sm, sc, fbxFile)
	fbx_meshes = GetMeshFromScene(sc)

	# foreach Texture
	for textureIndex in range (0, sc.GetTextureCount()):
		textureFileName = sc.GetTexture(textureIndex).GetFileName()
		if os.path.isfile(textureFileName):
			print textureFileName
		else:
			if os.path.isfile("%s.tga"%(fbxFile[:-4])):
				print "%s.tga"%(fbxFile[:-4])
			else:
				print "Can't find texture file %s from %s"%(sc.GetTexture(textureIndex).GetFileName(), fbxFile)


	# foreach Mesh
	for mesh in fbx_meshes:
		name, uvSet = GetUVSetFromMesh(mesh)[0]
		node = MeshUVNode(mesh, uvSet,
			Image.new("RGBA", sizes[random.randrange(0, len(sizes))], background_colors[random.randrange(0, len(background_colors))]))
		configure.nodes[UVSetNamer.Name()] = node

		print "mesh: %s"%(mesh.GetName())

		####
		# material
		for i in range(0, mesh.GetLayerCount()):
			print "texture: %s"%(mesh.GetLayer(i).GetTextures(FbxLayerElement.EType.TextureDiffuse))
		###

		# for every vertices,
		for vertexIndex in range(0, node.mesh.GetPolygonCount()*3):
			uv_point = uvSet.GetDirectArray().GetAt(vertexIndex)

			#
			UVPointTuple = (int(math.floor(node.image.size[0] * uv_point[0])), int(math.floor(node.image.size[1] * uv_point[1])))
			node.image.putpixel(UVPointTuple, color)


# initialize sdk
if dirname != "":
	if not os.path.exists(dirname):
		os.makedirs(dirname)
# 
fbxs = glob.glob("originals/*.fbx")
for fbx in fbxs:
	time_before_fbxread = time.time()
	packScene (fbx)
	print "Packing Scene: ", fbx, ":", (time.time() - time_before_fbxread)*1000, "miliseconds"

time_before_pack = time.time()

# Pack Atlas
packed = AtlasPack.Pack(configure)
print "Packing time: ", (time.time() - time_before_pack)*1000, "miliseconds"

# debug
packed.save("atlas.png")


for sm, sc, filename in managers_and_scenes_and_filenames:
	print "Save file : %s"%(filename)
	FbxCommon.SaveScene(sm, sc, dirname+"/"+os.path.basename(filename)[:-4]+".fbx")













