import frames

##LOOK IN UTILITY MODULE FOR IMAGE CACHE CODE... SHOULD USE IT WHEN STARTING TO GET OPTIONS

def GetImageData(type):
	if type is 'player':
		return player
	if type is 'standardBlock':
		return standardBlock
	else:
		return Default() #really here to not break stuff
		
#def GetAnimationData(type):

"""
frames.LoadFrames(startcoord-x, startcoord-y, file, tilesize-x, tilesize-y, total frames to get)
"""

def Miner():
	image = "images\\miner.png"
	framelist = frames.LoadFrames(0,0,image,16,16,4)

	animations = {
		'Left': [3],
		'Right': [2],
		'Down': [0], 
		'Up': [1],
		}
	
	data = {
			'animations': animations,
			'frames': framelist,
			}
	
	return data

miner = Miner()		
'''	
class SpriteMetaData:
	def __init__(self):
		self.animations = {}

		#Scale = 0
		#Rotation = 0
		#SpriteCollisions = 0
		#TileCollisions = 0
		#Alpha = 255
	
		#self.realX = 0
		#self.realY = 0
		
		#Map = 1
	
		self.Animations =   { 		
					"Down_Walk" : "z6 w8 z7 w8 z8 w8 z7 w8 /0",
					"Up_Walk" : "z9 w8 z10 w8 z11 w8 z10 w8 /0",
					"Right_Walk" : "z3 w8 z4 w8 z5 w8 z4 w8 /0",
					"Left_Walk" : "z0 w8 z1 w8 z2 w8 z1 w8 /0",
						
					"Up_Stand" : "z10",
					"Down_Stand" : "z7",
					"Left_Stand" : "z1",
					"Right_Stand" : "z4",
						
					"Up_Attack" : "z1 w4 z2 w4 z3 w4 z0 w4",
					"Down_Attack" : "z3 w2 z0 w2 z1 w2 z2 w2",
					"Left_Attack" : "z0 w2 z1 w2 z2 w2 z3 w2",
					"Right_Attack" : "z2 w2 z3 w2 z0 w2 z1 w2",

					"Up_Hurt" : "rgba255,255,255,255,255,0,0,100,35 w3 rgba255,0,0,100,255,255,255,255,35 w3 /2",
					"Down_Hurt" : "rgba255,255,255,255,255,0,0,100,35 w3 rgba255,0,0,100,255,255,255,255,35 w3 /2",
					"Left_Hurt" : "rgba255,255,255,255,255,0,0,100,35 w3 rgba255,0,0,100,255,255,255,255,35 w3 /2",
					"Right_Hurt" : "rgba255,255,255,255,255,0,0,100,35 w3 rgba255,0,0,100,255,255,255,255,35 w3 /2",
						
					"Up_Dead" : "rgba255,255,255,255,0,0,0,0,5 w4",
					"Down_Dead" : "rgba255,255,255,255,0,0,0,0,5 w4",
					"Left_Dead" : "rgba255,255,255,255,0,0,0,0,5 w4",
					"Right_Dead" : "rgba255,255,255,255,0,0,0,0,5 w4"
				}
		
'''