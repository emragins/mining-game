"""
Initial Backbone of code written by SDHawk... though heavily altered
"""

"""
Visual representation of an entity. Contains animation and walk scripts to control its apperance.
"""

import ika
#from collision import *
import utility
import animationdata
import imagedata
import box

def MakeSprite(parent, type):	
	'''
	frames = {} # Contains the sprite images. Note: Later iterations should store all 
			#sprite data in a single container for reference, as opposed to having multiple 
			#copies of every sprite floating around.
			
			Second thought... IF I were to make blanket sprite copies:
				-x/y okay, because not controlled by sprite
				-but would need to have different parents, hence, need different copies of sprites.
				-Also, would not want every sprite of each type to be in the same frame of animation.
	
			However: I *think*, presently, that new dicts are created each time a sprite is made, and those should be shared
				because they do not change.
	'''
	
	image = imagedata.GetImageData(type) 
	#GiveImageDataToParent(parent, image)
	
	sprite = Sprite(parent, image['frames'], image['animations'])
	
	return sprite
	
	
class Sprite:	
	def __init__(self, parent, frames, animations):
	
		self.parent = parent
		self.animations = animations
		self.currentAnimation = None
		self.frames = frames
		self.currentFrame = 0 #Current displayed image
		#self.layer = 0
		self.animationSpeed = 3
		self.currentLabel = 'WaitLeft'
		self.animationTimer = 0
		self.currentScriptFrame = 0
		self.map = True
		
	Color = ika.RGB(255,255,255,255) ##
	
	def Render(self):
		#Draws the sprite. 
		#Note: Add future optimizations to only draw it if it's in viewing distance.
		if self.map:
			x, y = utility.MapToScreen(self.parent.realX, self.parent.realY)
		else:
			x, y = self.parent.realX, self.parent.realY
		
		#if Alpha == 255:
		#	self.frames[self.currentFrame].Blit(xy[0], xy[1])
		#else:
		ika.Video.TintBlit(self.frames[self.currentFrame], x, y, self.Color)
		
	def Update(self):
		
		#determine which animation
		"""
		use the last animation given in extraStates, if it exists
		scenario: 
		player walks, set state
		player jumps, extra state
		player attacks, extra state 2 - this should be displayed
		"""
		extraStatesLen = len(self.parent.extraStates)
		if extraStatesLen != 0:
			newLabel = self.parent.extraStates[extraStatesLen-1]
		else:
			newLabel = self.parent.GetState()
		
		#Processess which animation
		if newLabel is not self.currentLabel and not newLabel in self.currentLabel:
			self.LabelChanged(newLabel)
			self.currentFrame = self.GetNextFrame()
			
		#update animation
		if self.animationTimer < self.animationSpeed:
			self.animationTimer += 1
		else:
			self.animationTimer = 0
			self.currentFrame = self.GetNextFrame()
	
	def LabelChanged(self, newLabel):
		self.animationTimer = 0
		if not newLabel in self.animations:
			if newLabel == 'Wait':
				if 'Left' in self.currentLabel:
					newLabel = 'WaitLeft'
				else:
					newLabel = 'WaitRight'
			elif newLabel == 'Jump':
				if 'Left' in self.currentLabel:
					newLabel = 'JumpLeft'
				else:
					newLabel = 'JumpRight'
			else:
				newLabel = self.currentLabel ##won't throw an error, but won't crash game
		self.currentLabel = newLabel
		
	def GetNextFrame(self):
		currentAnimationList = self.animations[self.currentLabel]
		if self.currentScriptFrame >= len(currentAnimationList) - 1:
			self.currentScriptFrame = 0
		else:
			self.currentScriptFrame += 1
		
		#gives int representing which frame in self.frames to use
		frame = currentAnimationList[self.currentScriptFrame] 
		
		return frame
	
	'''	
	def CheckTileCollision(self, x, y, treasure=0):
		#NOTE: Add a case for if the map isn't the active map.
		
		#HotW = self.Width-self.HotX
		#HotH = self.Height-self.HotY
		
		if x < 0 or y< 0:
			return 1
			
		if x >= ika.Map.GetLayerProperties(self.Layer)[1]*ika.Map.tilewidth or y >= ika.Map.GetLayerProperties(self.Layer)[2]*ika.Map.tileheight:
			return 1	

		Obstructed = 0
		OnObstructed = 0
		OffObstructed = 0
		
		COnObs = 1
		COffObs = 1
		self.Ladder = 0
		
		for Layer in range(0,6):
		
			CurTileX = self.parent.realX/ika.Map.tilewidth
			CurTileY = self.parent.realY/ika.Map.tileheight
			
			OnTile = ika.Map.GetTile(CurTileX, CurTileY, Layer)
			
			if x > self.parent.realX: #Going right
				OffTile = ika.Map.GetTile(CurTileX+1, CurTileY, Layer)
				NextTileX = CurTileX+1
				NextTileY = CurTileY
			elif x < self.parent.realX: #Going left
				OffTile = ika.Map.GetTile(CurTileX-1, CurTileY, Layer)
				NextTileX = CurTileX-1
				NextTileY = CurTileY			
			elif y > self.parent.realY: #going down
				OffTile = ika.Map.GetTile(CurTileX, CurTileY+1, Layer)
				NextTileX = CurTileX
				NextTileY = CurTileY+1
			elif y < self.parent.realY: #going up
				OffTile = ika.Map.GetTile(CurTileX, CurTileY-1, Layer)
				NextTileX = CurTileX
				NextTileY = CurTileY-1
			
			OnObs = engine.GetObs(OnTile)
			OffObs = engine.GetObs(OffTile)
			
			if OffObs is not None and OffObs.Ladder:
				return 0
			
			if OnObs is not None and OnObs.Ladder:
				OnObstructed = 0
				COnObs = 0
			
			if COnObs and OnObs is not None and OnObs.CheckCollision(NextTileX, NextTileY, CurTileX, CurTileY,0):
				OnObstructed = 1
			if COffObs and OffObs is not None and OffObs.CheckCollision(CurTileX, CurTileY, NextTileX, NextTileY,1):
				OffObstructed = 1
			
		
		if not treasure:	
			
			if OnObstructed or OffObstructed:
				return 1
			else:
				return 0	
		else:
			#Only check on obstructions if we're only checking to make sure there isn't an obstruction between us and a treasure chest.
			if OnObstructed:
				return 1
			else:
				return 0		
		
		#xy = [ [ x+self.HotX, y+self.HotY], 
		#	   [ x+self.HotX+self.HotW, y+self.HotY],
		#	   [ x+self.HotX, y+self.HotY+self.HotH],
		#	   [ x+self.HotX+self.HotW, y+self.HotY+self.HotH]]
		
		#if self.TileCollisions:
		#	if x+16 <= 0 or y+16 <= 0:
		#		return 1
				
		#	if x >= ika.Map.GetLayerProperties(self.Layer)[1]*ika.Map.tilewidth or y >= ika.Map.GetLayerProperties(self.Layer)[2]*ika.Map.tileheight:
		#		return 1
				
		#	for z in xy:
		#		z[0] = z[0]/ika.Map.tilewidth
		#		z[1] = z[1]/ika.Map.tileheight
				
		#	#xy = utility.PixelToTile([x,y])
			
		#	Obs = 0
			
		#	for z in xy:
		#		Obs += ika.Map.GetObs(z[0],z[1],self.Layer)
			
		#	return Obs
		#	#return ika.Map.GetObs(x/ika.Map.tilewidth,y/ika.Map.tileheight,self.Layer)
		#else:
		#	return 0
	'''
	'''
	def IsInArea(self,x,y,w,h):	
		
		ThisEntity = Box(self.parent.realX+self.HotX, self.parent.realY+self.HotY, self.HotW, self.HotH)
		
		if ThisEntity.CollidesWith(Box(x,y,w,h)):
			return 1
			
		return 0
		
	def IsInAreaNoHotSpots(self,x,y,w,h):	
		
		ThisEntity = Box(self.parent.realX, self.parent.realY, self.Width, self.Height)
		OtherEntity = Box(x,y,w,h)
		
		#print "["+str(self.parent.realX)+"-"+str(self.parent.realY)+"-"+str(self.Width)+"-"+str(self.Height)+"]---"+"["+str(x)+"-"+str(y)+"-"+str(w)+"-"+str(h)+"]"
		
		if OtherEntity.CollidesWith(ThisEntity):
			return 1
			
		return 0
	'''
	'''	
	def CheckCustomCollision(self, x, y, w, h):
	
		ThisEntity = Box(x,y,w,h)
			
		for map in engine.Maps:
			if self.Parent in map.Entities:
				for entity in map.Entities:
					s = entity.Sprite
						
					if entity != self.Parent and s.Layer == self.Layer and s.SpriteCollisions and ThisEntity.CollidesWith(Box(s.x+s.HotX,s.y+s.HotY,s.HotW,s.HotH)):
							
						return entity
							
		return 0	
	'''
	'''
	def CheckSpriteCollision(self, x, y):
		#HEY LET'S TRY TO BE MORE UNEFFICENT, OKAY?
		
		if self.SpriteCollisions:
		
			ThisEntity = Box(x+self.HotX, y+self.HotY, self.HotW, self.HotH)
			
			Collision = 0
			
			for map in engine.Maps:
				if self.Parent in map.Entities:
					for entity in map.Entities:
						s = entity.Sprite
						
						if entity != self.Parent and s.Layer == self.Layer and s.SpriteCollisions and ThisEntity.CollidesWith(Box(s.x+s.HotX,s.y+s.HotY,s.HotW,s.HotH)):
							

							entity.OnTouch(self.Parent)
							Collision = 1
							
			return Collision
			
		else:
			
			return 0
	'''
	'''
class BuildingSprite(Sprite):
	
	def __init__(self, parent, image, w, h, hx, hy, hw, hh):
		
		self.Parent = parent
		self.MoveScript = MoveScript(self)
		self.AnimationScript = AnimationScript(self)
		
		self.frames = [ utility.GetImage(image) ] 
		
		self.HotX =hx
		self.HotY = hy
		self.HotW = hw
		self.HotH = hh
		self.Width = w
		self.Height = h
		
		self.Animations =   { 
						
						"Down_Walk" : "z0 /0",
						"Up_Walk" : "z0 /0",
						"Right_Walk" : "z0 /0",
						"Left_Walk" : "z0 /0",
							
						"Up_Stand" : "z0 /0",
						"Down_Stand" : "z0 /0",
						"Left_Stand" : "z0 /0",
						"Right_Stand" : "z0 /0",
					}		
	'''
	