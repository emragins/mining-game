import ika
#Portions of the code originally created by Hatchet.

def LoadFrames(x,y,img, tileWidth, tileHeight, numtiles, padding = 0):    
	"""
	This is a simple function that takes any image that's formatted like a tileset and rips the tiles into a
	list which is then returned. 
	img: image to rip from
	tileWidth/tileHeight: tileWidth and tileHeight of a single tile
	span: how many tiles per row
	numtiles: number of tiles to rip
	padding: number of pixels between tiles
	"""
	tiles=[]
	bigImage = ika.Canvas(img)
	numFramesWide = int(bigImage.width /(tileWidth + padding)) 
	i2 = 0
	i3 = 0
	
	for i in range(numtiles):
		tile = ika.Canvas(tileWidth, tileHeight)
		bigImage.Clip( x+(i2*tileWidth + i2*padding), y+(i3*tileHeight+i3*padding) , tileWidth , tileHeight)
		#bigImage.Blit(tile, -1-((tileWidth+1)*(i%span)), -1-((tileHeight+1)*(i%span)), ika.Opaque)
		bigImage.Blit(tile, 0, 0, ika.Opaque)
		tiles.append(ika.Image(tile))
		
		i2+=1
		if i2 >= numFramesWide:
			i3+=1
			i2=0
	#ika.Exit(str(tiles))
	return tiles