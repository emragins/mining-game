import entity
import positionhandler
import sprite
import time
import ika 	#for time

class MovingEntity(entity.Entity, positionhandler.PositionHandler):
	def __init__(self, x, y, type, direction = "right"):
		entity.Entity.__init__(self, x, y, type)
		positionhandler.PositionHandler.__init__(self)
		self.sprite = sprite.MakeSprite(self, type)
		
		
		self.type = type
		self.currentState = 'Wait'
		self.direction = direction #used to determine actions such as 'make block' or 'attack'
			#updates with 'left' or 'right' movement
		self.extraStates = []
		self.falling = False
		self.timeLastMoved = ika.GetTime() + 20
		
	def Update(self):
		#print self ##
		#print 'hotspots', self.realX + self.hotX, self.realY + self.hotY ##
		oldRealX = self.realX
		oldRealY = self.realY
		
		print self
		print 'time', self.timeLastMoved, ika.GetTime()
		print 'old', oldRealX, oldRealY
		if self.timeLastMoved + 20 > ika.GetTime() or self.type is 'player':
			positionhandler.PositionHandler.Update(self)
		
		entity.Entity.Update(self)
		
		self.sprite.Update()
		print 'new', self.realX, self.realY
		if self.realX is not oldRealX or self.realY is not oldRealY:
			print 'bleh', self.timeLastMoved
			self.timeLastMoved = ika.GetTime()
		
	def Render(self):
		self.sprite.Render()
	
	def GetPosition(self):
		return self.realX, self.realY	
	
	"""	
	Possible States:
	MoveLeft
	MoveRight
	Wait | WaitLeft, WaitRight - for sprite ONLY
	Jump | JumpLeft, JumpRight - for sprite ONLY
	GrabLeft
	GrabRight
	"""
	
	def SetState(self, state):
		if self.currentState is state:
			pass
		else:
			self.currentState = state
			self.SetDirectionFromState(state)
			
	def GetState(self):
		return self.currentState
	
	def AddState(self, state):
		if not state in self.extraStates:
			self.extraStates.append(state)
	def RemoveState(self, state):
		if state in	self.extraStates: #(for error checking)
			self.extraStates.remove(state)
			
	def SetDirectionFromState(self, state):
		##should be able to make this better
		if self.direction in state:
			return
		elif 'Right' in state:
			self.direction = 'Right'
		elif 'Left' in state:
			self.direction = 'Left'
		else:
			pass
	#should probably be only in normal Entity (despite it being movement.. it is stat based)
	def GetJumpStrength(self):
		return self.stats.jumpStrength
	
	def StopFalling(self):
		self.falling = False
	def StartFalling(self):
		self.falling = True
	def IsFalling(self):
		return self.falling