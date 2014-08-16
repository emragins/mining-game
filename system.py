import sys
sys.path = ['','source', 'python'] 

import ika


last_fps = 0
TILESIZE = 16
OFFSET_X = 16
OFFSET_Y = 48
'''
possibleMinerals = ["Hematite", 'Gold', 'Copper', "Quartz","Rhodochrosite", "Garnet", "Sillimanite", "Staurolite", "Flourite",  "Babingtonite", "Galena", "Silver", "Beryl", "Bowanite", "Rose Quartz", "Talc"]
''' 

common = ["Coal", "Lead", "Iron"]
semi = ["Copper", "Quartz", "Silver"]
rare = ["Gold"]
special = ["Axe", "Food"]
#initialize shit
score = 0

drawList = []
updateList = []

class Grid(object):
	def __init__(self, num_col= 20, num_rows = 20):
		self.grid = []
		self.num_col = num_col
		self.num_rows = num_rows
		
		
		#fill grid
		for column in range(0,num_col):
			row = []
			for x in range(0,num_rows):
				row.append(MakeTile())
				
			self.grid.append(row)

	def Draw(self):
		x1 = OFFSET_X
		x2 = x1 + TILESIZE
		y1 = OFFSET_Y
		y2 = y1 + TILESIZE
		for col in self.grid:
			for tile in col:
				y2 = y1 + TILESIZE
				grey_scale = 15+(tile.structure*16)
				ika.Video.DrawRect(x1,y1,x2,y2, ika.RGB(grey_scale,grey_scale,grey_scale), 1)
				if tile.rarity == "N":
					pass
				elif tile.rarity == "C":
					ika.Video.DrawRect(x1,y1,x2,y2, ika.RGB(200,80,0), 0) #brown
				elif tile.rarity == "S":
					ika.Video.DrawRect(x1,y1,x2,y2, ika.RGB(220,215,24), 0) #yellowish
				elif tile.rarity == "R":
					ika.Video.DrawRect(x1,y1,x2,y2, ika.RGB(215,9,173), 0) #pinkish
				#''' REMOVED SO THAT "POWER-UPS" ARE HIDDEN
				elif tile.rarity == "X":
					ika.Video.DrawRect(x1,y1,x2,y2, ika.RGB(0,255,0), 0) #green
				#'''
				y1 += TILESIZE + 1
				
			x1 = x2 + 1
			x2 = x1 + TILESIZE
			
			y1 = OFFSET_Y
				
	def Update(self):
		pass
		
	def DestroyTile(self, x, y):
		tile = self.grid[x][y]
		tile.structure = 0
		tile.mineral = 0
		tile.rarity = "N"
		
	def Mine(self, x, y, atk):
		#check if even doable
		if x < 0 or x >= self.num_col:
			return False
		if y < 0 or y >= self.num_rows:
			return False
		
		
		global score
		
		tile = self.grid[x][y]
		if tile.structure == 0:
			return False	##MAKE THIS TRUE TO MAKE STR GO DOWN EACH "SWING"
			
		if atk >= tile.structure:
			tile.structure = 0
			
			if tile.rarity == "N":
				score += 5
			elif tile.rarity == "C":
				score += 10
			elif tile.rarity == "S":
				score += 20
			elif tile.rarity == "R":
				score += 30
			elif tile.rarity == "X":
				if tile.mineral == "Axe":
					miner.atk += 2
					PopUp("Your axe is sharper now!")
				elif tile.mineral == "Food":
					miner.str += 10
					PopUp("You found some yummy worms!")
					
			tile.rarity = "N"
			tile.mineral = "Nothing"
			
		else:
			tile.structure -= atk
		
		return True
		
	def IsWalkable(self, x, y):
		#check if even doable
		if x < 0 or x >= self.num_col:
			return False
		if y < 0 or y >= self.num_rows:
			return False
		
		tile = self.grid[x][y]
		if tile.structure == 0:
			return True
		
	def HasItem(self):
		if self.item != None:
			return self.item
	
#ika.Random(min, max) :: min <= x < max

def MakeTile():
	structure = ika.Random(1,6) +ika.Random(1,6) +ika.Random(1,6) #3d5
	a = ika.Random(1,4)
	rarity = "N"
	mineral = "Nothing"
	item = None
	if a == 1:
		b = ika.Random(1,10)
		if b in [1,2,3,4]:
			c = ika.Random(0,len(common))
			mineral = common[c]
			rarity = "C"
		elif b in [4,5,6]:
			c = ika.Random(0,len(semi))
			mineral = semi[c]
			rarity = "S"
		elif b in [7,8]:
			c = ika.Random(0,len(rare))
			mineral = rare[c]
			rarity = "R"
		elif b in [9]:
			c = ika.Random(0,len(special))
			mineral = special[c]
			rarity = "X"
			item = True
			
	return Tile(structure, mineral, rarity, item)
		
class Tile(object):
	def __init__(self, structure = 11, mineral = "Nothing", rarity = "N", item = None):
		self.structure = structure
		self.mineral = mineral
		self.rarity = rarity
		self.item = item
		
class Miner(object):
	"""
	location
	has sprite
	
	holds pickaxe
	can mine
	
	no inventory--scores as he mines
	"""
	
	def __init__(self):
		global grid
		global TILESIZE
		
		#--image stuff--
		import imagedata
		self.imagedata = imagedata.miner
		"""
		data = {
			'animations': animations,
				Dictionary with frames ::"Left", "Right", "Up", "Down"
			'frames': framelist,
				::list of pre-cut images to use with animations
			}
		"""
		
		#--location stuff--
		self.x = 10
		self.y = 0
		
		grid.DestroyTile(self.x,self.y)
		self.facing = "Down"
		
		#--other stuff--
		self.str = 100
		self.atk = 5
		
	def Draw(self):
		realx = OFFSET_X + self.x * (TILESIZE+1)
		realy = OFFSET_Y + self.y * (TILESIZE+1)
		
		loc = self.imagedata["animations"][self.facing][0]	##hardcodes first frame.. no animation
		ika.Video.Blit(self.imagedata["frames"][loc], realx, realy)
		
	def Update(self):
		#needs input from human
		kb = ika.Input.keyboard
			
		move = False
		
		if kb['LEFT'].Pressed():
			self.facing = "Left"
			move = True
		elif kb['RIGHT'].Pressed():
			self.facing = "Right"
			move = True
		elif kb['UP'].Pressed():
			self.facing = "Up"
			move = True
		elif kb['DOWN'].Pressed():
			self.facing = "Down"
			move = True
		
		if kb["F5"].Pressed():
			Restart()
		
		#determine which square miner is facing
		targetx = self.x
		targety = self.y
		if self.facing == "Left":
			targetx -= 1
		elif self.facing == "Right":
			targetx += 1
		elif self.facing =="Down":
			targety += 1
		elif self.facing == "Up":
			targety -= 1
		
		#act if needed
		if move:
			if grid.IsWalkable(targetx, targety):
				self.x = targetx
				self.y = targety
			
		if kb['SPACE'].Pressed():
			mined = grid.Mine(targetx, targety, self.atk)	
			if mined:
				self.str -= 1
				if self.str <= 0:
					GameOver()
					
class Display(object):
	def __init__(self):
		self.font = ika.Font("ocr_grey.fnt")
	def Draw(self):
		global score
		global miner
		self.font.Print(5,5, "Strength: " + str(miner.str))
		self.font.Print(5,20, "Score: " + str(score))

class PopUp(object):
	def __init__(self, text):
		self.font = ika.Font("ocr_grey.fnt")
		self.time = ika.GetTime()
		self.text = text
		drawList.append(self)
		updateList.append(self)
	def Draw(self):
		self.font.RightPrint(395,5, self.text)
	def Update(self):
		if self.time + 100 <= ika.GetTime():
			drawList.remove(self)
			updateList.remove(self)

def GameOver():
	PopUp("Too Tired. F5 to restart.")
	

def RunGame():
	global drawList
	global updateList
	last_update = 0
		
	while 1:
		if ika.GetTime() > last_update:
			global last_fps
			
			last_update = ika.GetTime()+1
			
			if last_fps != ika.GetFrameRate():
				ika.SetCaption( "Bergbau (FPS: "+str(ika.GetFrameRate())+")" )
				last_fps = ika.GetFrameRate()
			
			ika.Input.Update()
			#update shit
			for updateable in updateList:
				updateable.Update()
	
			#ika.ProcessEntities()
		
		ika.Render()
		#draw shit
		for drawable in drawList:
			drawable.Draw()
			
	
		ika.Video.ShowPage()
	
#--Create actual objects---
grid = Grid(20,20)
drawList.append(grid)

miner = Miner()
drawList.append(miner)
updateList.append(miner)

display = Display()
drawList.append(display)		

def Restart():
	global drawList 
	global updateList
	drawList = []
	updateList = []
	
	global grid
	grid = Grid(20,20)
	drawList.append(grid)
	
	global miner
	miner = Miner()
	drawList.append(miner)
	updateList.append(miner)

	global display
	display = Display()
	drawList.append(display)		

#--Start the game----
RunGame()