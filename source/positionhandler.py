
import collisions
#from data import configdata #need for quadrant checking
		
class PositionHandler(object):
	def __init__(self):
		self.moveSpeed = self.GetMoveSpeed()
		self.states = {
			'MoveLeft': self.MoveLeft,
			'MoveRight': self.MoveRight,
			'Wait': self.Wait,
			'Jump': self.Jump,
			'GrabLeft': self.Wait,
			'GrabRight': self.Wait,
			None: self.Wait
			
			}
		
		self.vertNegativeSpeed = 1 #positive is down
		self.gravityTimer = 0
		self.gravityEffect = 1
		self.lastGravityCollision = None
		
		
		
	def Update(self):
		state = self.states[self.GetState()]
		state()
		for state in self.extraStates:
			self.states[state]()
		self.ApplyGravity()	
		
	def Wait(self):
		pass	
	
	"""
	hasattr...
	need to return somehow to player and enemies (for ai purposes) what it collided with. 
	player will need blocks and items, enemies will need anything solid so they can turn around if moving, or climb even
	
	could maybe be more specific instead of just "collidesWith" could use "collidesWithBlock", "collidesWithItem" saving it from testing walls, too
	"""
	def MoveLeft(self):
		self.realX -= self.moveSpeed	
		if hasattr(self, "collidesWithBlock"): #should only be for anything where a collision is meaningful. ie. Block won't use this
			self.collidesWithBlock = collisions.CheckCollisionsBlocks(self)	##maybe change to just not block... o		
		col = collisions.CheckSolidCollisionsForMovement(self)
		if hasattr(col, "realX"):
			while self.CollidesWith(col):  ##might break if collision adjustment moves from one object to the next
				self.realX += 1
		else:
			while collisions.CheckSolidCollisionsForMovement(self):
				self.realX += 1
				
	def MoveRight(self):
		self.realX += self.moveSpeed
		if hasattr(self, "collidesWithBlock"): #should only be for anything where a collision is meaningful
			self.collidesWithBlock = collisions.CheckCollisionsBlocks(self)
		col = collisions.CheckSolidCollisionsForMovement(self)
		if hasattr(col, "realX"):
			while self.CollidesWith(col):  ##might break if collision adjustment moves from one object to the next
				self.realX -= 1
		else:
			while collisions.CheckSolidCollisionsForMovement(self):
				self.realX -= 1
		
	
	"""Used for being moved by something other than interal power"""
	def MoveLeftBy(self, speed):
		self.realX -= speed	
		col = collisions.CheckSolidCollisionsForMovement(self)
		if hasattr(col, "realX"):
			while self.CollidesWith(col):  ##might break if collision adjustment moves from one object to the next
				self.realX += 1
		else:
			while collisions.CheckSolidCollisionsForMovement(self):
				self.realX += 1
		return col
	def MoveRightBy(self, speed):
		self.realX += speed
		col = collisions.CheckSolidCollisionsForMovement(self)
		if hasattr(col, "realX"):
			while self.CollidesWith(col):  ##might break if collision adjustment moves from one object to the next
				self.realX -= 1
		else:
			while collisions.CheckSolidCollisionsForMovement(self):
				self.realX -= 1
		return col
		
	def Jump(self):			
		if hasattr(self, "DropBlock"): #should only be for anything where a collision is meaningful
			self.DropBlock()
		self.realY -= self.GetJumpStrength()
		collides = collisions.CheckSolidCollisionsForMovement(self)
				
		if collides or not self.IsFalling():
			while collisions.CheckSolidCollisionsForMovement(self):
				self.realY += 1 #move down incrementally to get head out of ceiling
			self.RemoveState('Jump') #remove the state so that verticle propultion is 0 (ie. so it can just start falling)
			
	
	##MUST ADD STUFF TO DISTINGUISH BETWEEN WALLS AND OTHER ENTITIES... PROBABLY EASIEST TO DO WITH LAYERS
	def ApplyGravity(self):
		self.realY += self.vertNegativeSpeed
		self.lastGravityCollision = collisions.CheckSolidCollisionsForGravity(self)
		while collisions.CheckSolidCollisionsForGravity(self):
			self.realY -= 1 #move up incrementally to 'land' on the ground
				
		if not self.lastGravityCollision:
			self.gravityTimer += 1
			self.StartFalling()
			if self.gravityTimer >= 3: # and self.vertNegativeSpeed < 15:
				self.vertNegativeSpeed += self.gravityEffect
				self.gravityTimer = 0
		else:
			self.vertNegativeSpeed = 1
			self.gravityTimer = 0
			self.StopFalling()
			self.RemoveState('Jump')  #needed here because otherwise char will bounce will lands due to order
		
		
	def GetOpenQuadrantsLeft(self): #return list of specific number of open quadrants/tiles	
		pass
		'''
		pseudocode:
		numQuadrants = int(self.height/configdata.tilesize)
		list = []
		for i in range(numQuadrants):
			establish real x/y coordinates
			establish tile x/y coordinates
			establish if tile is obstructed
			if tile obstructed:
				list.append(i) #note: want the quadrant, NOT the real or tile x/y
		
		return list	
		'''
		
		
		