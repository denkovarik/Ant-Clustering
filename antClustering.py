from PIL import Image, ImageDraw
import cv2
import math
import numpy as np
import random
import time
import sys, signal, os, threading
from builtins import IOError



global t
t = 0



'''
This is the signal handler that will save the current populations to seperate
files when a keyboard interrupt is incountered.
'''
def signal_handler(signal, frame):
	global t
	print("saving image")
	ext = ".png"
	name = "Run ID: "+str(runId)+" Final image "+str(t)+" iterations"+ext
	image = paintImage(room, colony, 3,0)
	cv2.imwrite(dirName + name,image)
	#showRoom(image, name, 1)
	cv2.destroyAllWindows()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


'''
Catches ctrl z
'''
def handler(signum, frame):
	cv2.destroyAllWindows()
	sys.exit(0)

signal.signal(signal.SIGTSTP, handler)



class Environment:
	def initAntLoc():
		antLoc = list(())
		for i in range(200):
			antLoc.append(list(()))
			for j in range(200):
				antLoc[i].append(None)
		return antLoc
	width = 200
	height = 200
	theRoom = np.zeros((height,width,3), np.uint8)	
	theRoom[:,0:width] = (0,0,0)      # (B, G, R)
	antLoc = initAntLoc()



class Ant:
	col = 0
	row = 0
	loaded = 0
	obj = tuple((0,0,0))
	direction = 1
	persist = 0


c = 0

'''
This function will paint the image.
'''
def paintImage(room, colony, scale, showAnts):
	space = (0,0,0)
	red = [0,0,255]
	# make a blank image for the text, initialized to transparent text color
	image = np.zeros((room.width*scale,room.height*scale,3), np.uint8)	
	image[:,0:room.width*scale] = (255,255,255)      # (B, G, R)

	# Draw ants
	for x in colony:
		if showAnts == 1:
			cv2.circle(image,(x.col*scale,x.row*scale), 2, (19,69,139), -1)
		if x.loaded == 1:
			cv2.circle(image,(x.col*scale,x.row*scale), 2, (19,69,139), -1)
			if x.obj == (0,0,255):
				cv2.rectangle(image,(x.col*scale,x.row*scale),((x.col+1)*scale,
					(x.row+1)*scale),(0,0,255),-1)
			elif x.obj == (255,0,0):
				cv2.rectangle(image,(x.col*scale,x.row*scale),((x.col+1)*scale,
					(x.row+1)*scale),(255,0,0),-1)

	# Draw object in room
	i = 0
	j = 0
	while i < room.height:
		while j < room.width:
			if room.theRoom[j][i][2] == 255:
				cv2.rectangle(image,(j*scale,i*scale),((j+1)*scale,(i+1)*scale)
					,(0,0,255),-1)
			elif room.theRoom[j][i][0] == 255:
				cv2.rectangle(image,(j*scale,i*scale),((j+1)*scale,(i+1)*scale)
					,(255,0,0),-1)
			j = j + 1
		i = i + 1
		j = 0

	return image



def showRoom(image, name, wait):

	if wait == 1:
		cv2.imshow(name,image)
		k = cv2.waitKey(0)
	else:
		cv2.imshow(name,image)
		k = cv2.waitKey(1)

	if t % 1000 == 0 and t > 0:
		time.sleep(1)

	return



'''
This function will place 200 objects on the environment image 'the room', 100 
red with the other 100 blue.
'''
def makeMess(room):
	numObjects = 0
	redObj = (0,0,255)
	blueObj = (255,0,0)

	while numObjects < 100:
		row = random.randint(0,room.height-1)
		col = random.randint(0,room.width-1)

		# Place red objects on floor
		if room.theRoom[col][row][0] == 0 and room.theRoom[col][row][2] == 0:
			room.theRoom[col][row] = redObj
			numObjects = numObjects + 1

	numObjects = 0

	while numObjects < 100:
		row = random.randint(0,room.height-1)
		col = random.randint(0,room.width-1)

		# Place blue objects on floor
		if room.theRoom[col][row][0] == 0 and room.theRoom[col][row][2] == 0:
			room.theRoom[col][row] = blueObj
			numObjects = numObjects + 1

	return room



'''
This function will create and initialize a colony of ants
'''
def makeColony(room):
	colony = list(())
	#image = np.zeros((width,height,3), np.uint8)	

	while len(colony) < 500:
		row = int(room.height / 2)
		col = int(room.width / 2)

		#if image[col][row][0] == 0:
		newAnt = Ant()
		newAnt.row = row
		newAnt.col = col
		newAnt.loaded = 0
		room.antLoc[col][row] = newAnt
		colony.append(newAnt)
			
	return colony



def moveUp(direction, ant, room):
	if 	(
			direction == 1 and ant.row - 1 >= 0 
			and room.antLoc[ant.col][ant.row-1] == None
		):
		room.antLoc[ant.col][ant.row] = None
		ant.row = ant.row - 1			
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 1
		return True
	return False



def moveDown(direction, ant, room):
	if 	(
			direction == 2 and ant.row + 1 < room.height 
			and room.antLoc[ant.col][ant.row+1] == None
		):
		room.antLoc[ant.col][ant.row] = None
		ant.row = ant.row + 1			
		ant.direction = 2
		room.antLoc[ant.col][ant.row] = ant
		return True
	return False



def moveLeft(direction, ant, room):
	if 	(
			direction == 3 and ant.col - 1 >= 0 
			and room.antLoc[ant.col-1][ant.row] == None
		):
		room.antLoc[ant.col][ant.row] = None
		ant.col = ant.col - 1			
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 3
		return True
	return False



def moveRight(direction, ant, room):
	if 	(
			direction == 4 and ant.col + 1 < room.width 
			and room.antLoc[ant.col+1][ant.row] == None
		):
		room.antLoc[ant.col][ant.row] = None
		ant.col = ant.col + 1			
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 4
		return True
	return False



def moveUpLeft(direction, ant, room):
	if 	(
			direction == 5 and ant.col - 1 >= 0 and ant.row - 1 >= 0 
			and room.antLoc[ant.col-1][ant.row-1] == None
		):		
		room.antLoc[ant.col][ant.row] = None
		ant.row = ant.row - 1		
		ant.col = ant.col - 1	
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 5
		return True
	return False



def moveDownRight(direction, ant, room):
	if 	(
			direction == 6 and ant.col + 1 < room.width 
			and ant.row + 1 < room.height 
			and room.antLoc[ant.col+1][ant.row+1] == None
		):		
		room.antLoc[ant.col][ant.row] = None
		ant.row = ant.row + 1			
		ant.col = ant.col + 1
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 6
		return True
	return False



def moveDownLeft(direction, ant, room):
	if 	(
			direction == 7 and ant.col - 1 >= 0 and ant.row + 1 < room.height 
			and room.antLoc[ant.col-1][ant.row+1] == None
		):		
		room.antLoc[ant.col][ant.row] = None
		ant.col = ant.col - 1			
		ant.row = ant.row + 1
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 7
		return True
	return False



def moveUpRight(direction, ant, room):
	if 	(
			direction == 8 and ant.col + 1 < room.width and ant.row - 1 >= 0 
			and room.antLoc[ant.col+1][ant.row-1] == None
		):		
		room.antLoc[ant.col][ant.row] = None
		ant.col = ant.col + 1
		ant.row = ant.row - 1			
		room.antLoc[ant.col][ant.row] = ant
		ant.direction = 8
		return True
	return False



'''
This function will move the entire colony of ants
'''
def moveAnts(room, colony):
	space = (0,0,0)

	for x in colony:
		count = 0
		# Pick up item?
		localDensity = calcLocalDensity(room.theRoom[x.col][x.row], x.col, 
			x.row, room)
		if 	(
				room.theRoom[x.col][x.row][0] > 0 
				or room.theRoom[x.col][x.row][2] > 0 and x.loaded == 0
			):
			localDensity = calcLocalDensity(room.theRoom[x.col][x.row], x.col, 
				x.row, room)
			if pickUp(localDensity):
				x.loaded = 1
				x.obj = tuple((room.theRoom[x.col][x.row]))
				room.theRoom[x.col][x.row] = space
		# Drop item?
		elif(
				x.loaded == 1 and room.theRoom[x.col][x.row][0] == 0 
				and room.theRoom[x.col][x.row][2] == 0
			):
			localDensity = calcLocalDensity(x.obj, x.col, x.row, room)
			if dropIt(localDensity):
				x.loaded = 0
				room.theRoom[x.col][x.row] = tuple((x.obj))
				x.obj = (0,0,0)

		# move up
		if moveUp(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		# move down
		elif moveDown(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		# move left
		elif moveLeft(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		# move right
		elif moveRight(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		# move up right
		elif moveUpRight(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		# move up left
		elif moveUpLeft(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		#move down left
		elif moveDownLeft(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		# move down right
		elif moveDownRight(x.direction,x,room) and x.persist > 0:
			x.persist = x.persist - 1
		else:
			x.persist = random.randint(1,10)
			while count < 5:
				d = random.randint(1,8)
				# move up
				if moveUp(d,x,room) and x.persist > 0:
					count = 5
				# move down
				elif moveDown(d,x,room) and x.persist > 0:
					count = 5
				# move left
				elif moveLeft(d,x,room) and x.persist > 0:
					count = 5
				# move right
				elif moveRight(d,x,room) and x.persist > 0:
					count = 5
				# move up right
				elif moveUpRight(d,x,room) and x.persist > 0:
					count = 5
				# move up left
				elif moveUpLeft(d,x,room) and x.persist > 0:
					count = 5
				#move down left
				elif moveDownLeft(d,x,room) and x.persist > 0:
					count = 5
				# move down right
				elif moveDownRight(d,x,room) and x.persist > 0:
					count = 5
				count = count + 1	
	
	return colony



'''
This function will determine if an ant will pick up an item based on probability
'''	
def pickUp(localDensity):
	k = 0.1
	pp = (float(k) / (k + localDensity)) * (float(k) / (k + localDensity))
	r = random.random()
	
	if pp > r:
		return True
	return False 



'''
This function will determine if an ant will drop an item based on probability
'''	
def dropIt(localDensity):
    k = 0.5

    if localDensity > k:
        return True

    r = random.random()
    pd = 2 * localDensity

    if pd >= r:
        return True

    return False 



'''
This function will find the local density of like items.
'''
def calcLocalDensity(obj, x, y, room):
	density = 0.0
	s = 5
	obj = tuple((obj))
	objColor = 'w'
	a = 10

	if int(obj[0]) > 0:
		objColor = 'b'
	elif int(obj[2]) > 0:
		objColor = 'r'

	startx = x - s
	starty = y - s
	curx = startx
	cury = starty
	endx = x + s
	endy = y + s

	if curx < 0: 
		curx = 0

	if cury < 0: 
		cury = 0
	
	if endx > room.width - 1:
		endx = room.width - 1

	if endy > room.height - 1:
		endy = room.height - 1

	while cury <= endy:
		while curx <= endx:
			if objColor == 'r' and not(curx == x and cury == y):
				if room.theRoom[curx][cury][2] > 0:
					density = density + (1 - d(x,y,curx,cury) / a)
				elif room.theRoom[curx][cury][0] > 0:
					density = density - (1 - d(x,y,curx,cury) / a)
				if	(
						room.antLoc[curx][cury] != None 
						and room.antLoc[curx][cury].obj[2] > 0
					):
					density = density + (1 - d(x,y,curx,cury) / a)
				elif(
						room.antLoc[curx][cury] != None 
						and room.antLoc[curx][cury].obj[0] > 0
					):
					density = density - (1 - d(x,y,curx,cury) / a)
			elif objColor == 'b' and not(curx == x and cury == y):
				if room.theRoom[curx][cury][0] > 0:
					density = density + (1 - d(x,y,curx,cury) / a)
				elif room.theRoom[curx][cury][2] > 0:
					density = density - (1 - d(x,y,curx,cury) / a)
				if 	(
						room.antLoc[curx][cury] != None 
						and room.antLoc[curx][cury].obj[0] > 0
					):
					density = density + (1 - d(x,y,curx,cury) / a)
				elif(
						room.antLoc[curx][cury] != None 
						and room.antLoc[curx][cury].obj[2] > 0
					):
					density = density - (1 - d(x,y,curx,cury) / a)
			curx = curx + 1
		curx = startx
		cury = cury + 1
	density = density * (float(1) / (s*s))


	if density < 0:
		density = 0

	return density



'''
This function will calculate the euclidean distance between two points
'''
def d(x1, y1,  x2, y2):
	return  abs(x2 - x1) + abs(y2 - y1)


'''
This function will read the previous runID from the file and return the new 
runID
'''
def readRunId():
	try:
		f = open("runID.txt", "r")
		runId = int(f.readline()) + 1
	except IOError:
		runId = 1
	
	return runId



'''
This function will save the current runID to file
'''
def saveRunId(runID):
	fout = open("runID.txt", "w")
	fout.write(str(runID))
	return


runId = readRunId()
saveRunId(runId)
dirName = "images/"
ext = ".png"
name = "Run ID: " + str(runId) + " Start image" + " " + str(t) + " iterations" + ext
colony = list(())
room = Environment()
room = makeMess(room)
image = paintImage(room, colony, 3,0)
cv2.imwrite(dirName + name,image)
#showRoom(image,name,1)
colony = makeColony(room)

#cv2.namedWindow('Ant Clustering Simulation', 0)
image = paintImage(room, colony, 3,1)
showRoom(image,'Ant Clustering Simulation',0)
k = cv2.waitKey(1)

#while True:
while cv2.getWindowProperty('Ant Clustering Simulation', 1) == 1:
	colony = moveAnts(room, colony)
	image = paintImage(room, colony, 3,1)
	showRoom(image,'Ant Clustering Simulation',0)
	t = t + 1

cv2.destroyAllWindows()
name = "Run ID: " + str(runId) + " Final image " + " " + str(t) + " iterations" + ext
image = paintImage(room, colony, 3, 0)
showRoom(image,name,1)
saveRunId(runId)
cv2.imwrite(dirName + name,image)
print("saved ", name)
cv2.destroyAllWindows()
