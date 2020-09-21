import sys, pygame, time, matplotlib.pyplot as plt, keyboard, math
pygame.init()

n = 4
class sc():
	def __init__(self,x,y,n):
		self.n = n
		self.x = x
		self.y = y
		self.c = 1
	def n_ch(self, x):
		self.n += x
		if self.n < 0.1:
			self.n = 0.1 
	def x_ch(self, x):
		self.x += x
	def y_ch(self, x):
		self.y += x
	def zero(self):
		self.x=990
		self.y=540
		self.n=1
	def center(self,c):
		self.c = c
	def wait(self):
		keyboard.add_hotkey('+',lambda: self.n_ch(-1))
		keyboard.add_hotkey('-',lambda: self.n_ch(1))
		keyboard.add_hotkey('left arrow',lambda: self.x_ch(1))
		keyboard.add_hotkey('right arrow',lambda: self.x_ch(-1))
		keyboard.add_hotkey('up arrow',lambda: self.y_ch(1))
		keyboard.add_hotkey('down arrow',lambda: self.y_ch(-1))
		keyboard.add_hotkey('0',lambda:self.zero())
		for i in range(10):
			keyboard.add_hotkey('ctrl + ' + str(i),self.center,args=([i]))
		keyboard.add_hotkey('ctrl + m',lambda: self.center(-1))

class obect():
	def __init__(self, image, mass, speed, x, y):
		self.m = mass
		if image != None and image != 0:
			self.mg = pygame.image.load(image)
			self.rect = self.mg.get_rect()
			self.rect.top = y - (self.rect.height/2)
			self.rect.left = x - (self.rect.width/2)
		self.x = x
		self.y = y
		self.speed = speed
		self.speed.append((self.speed[0]**2 + self.speed[1]**2)**0.5)
	
	def move(self,speed = None):
		
		self.x += speed[0] if speed != None else self.speed[0]
		self.y += speed[1] if speed != None else self.speed[1]
		self.rect.left = int((self.x - (self.rect.width*ms.n/2)) /ms.n)
		self.rect.top = int((self.y - (self.rect.height*ms.n/2)) /ms.n)
		return self
	def __sub__(self,other):
		res = obect(0,0,[0,0],0,0)
		res.x = (self.x * self.m - other.x * other.m) / (self.m - other.m)
		res.x = round(res.x,5)
		res.y = (self.y * self.m - other.y * other.m) / (self.m - other.m)
		res.y = round(res.y,5)
		res.m = self.m - other.m
		return res
	def react(self,*others):
		others = list(others)
		if others == []: return
		if type(others[0]) == list:
			others.extend(list(others[0]))
			others.pop(0)
		for other in others:
			r = ((other.x - self.x)**2 + (other.y-self.y)**2)**0.5
			if r != 0:
				self.speed[0] += other.m/r**2 * (other.x-self.x)/r
				self.speed[0] = round(self.speed[0],5)
				self.speed[1] += other.m/r**2 * (other.y-self.y)/r
				self.speed[1] = round(self.speed[1],5)
				self.speed[2] = (self.speed[0]**2 + self.speed[1]**2)**0.5
	def mass_center(*balls):
		balls = list(balls)
		if balls == []: return
		if type(balls[0]) == list or type(balls[0]) == obect_list:
			balls.extend(list(balls[0]))
			balls.pop(0)
		res = obect(0,0,[0,0],0,0)
		for ball in balls:
			res.m += ball.m
			res.x += ball.x * ball.m
			res.y += ball.y * ball.m
		res.x /= res.m if res.m != 0 else 1
		res.x=round(res.x,5)
		res.y /= res.m if res.m != 0 else 1
		res.y = round(res.y,5)
		return res

class obect_list(list):
	def check(self):
		for i in self:
			if type(i) != obect:
				return list(self)
	def react(self):
		for subect in self:
			f = [0,0]
			for obbect in self:
				r = ((obbect.x - subect.x)**2 + (obbect.y-subect.y)**2)**0.5
				if r == 0:
					continue
				subect.speed[0] += obbect.m/r**2 * (obbect.x-subect.x)/r
				subect.speed[0] = round(subect.speed[0],5)
				subect.speed[1] += obbect.m/r**2 * (obbect.y-subect.y)/r
				subect.speed[1] = round(subect.speed[1],5)
				subect.speed[2] = (subect.speed[0]**2 + subect.speed[1]**2)**0.5
				
				critical_distance = ((obbect.rect.width**2 + obbect.rect.height**2)**0.5 + (subect.rect.width**2 + subect.rect.height**2)**0.5)/2
				if r < critical_distance:
					subect.x = (subect.x * subect.m + obbect.x * obbect.m) / (subect.m + obbect.m)
					subect.y = (subect.y * subect.m + obbect.y * obbect.m) / (subect.m + obbect.m)
					subect.speed[0] = (subect.speed[0] * subect.m + obbect.speed[0] * obbect.m) / (subect.m + obbect.m)
					subect.speed[1] = (subect.speed[1] * subect.m + obbect.speed[1] * obbect.m) / (subect.m + obbect.m)
					subect.speed[2] = (subect.speed[0]**2 + subect.speed[1]**2)**0.5
					subect.m += obbect.m
					self.remove(obbect)
				
		return self
	def move (self):
		for obbect in self:
			obbect = obbect.move()
		return self

class rocket(obect):
	def __init__(self, image, mass, speed, x, y, engm, engf, angle):
		obect.__init__(self, image, mass, speed, x, y)
		self.engm = engm
		self.engf = engf
		self.m += engm
		self.angl = angle
	def eng(self):
		self.speed[0] += self.engf/self.m *(math.cos(self.angl/360 * 2 * math.pi))
		self.speed[1] += self.engf/self.m *(math.sin(self.angl/360 * 2 * math.pi))
		self.speed[2] = (self.speed[0]**2 + self.speed[1]**2)**0.5
		print('speeding')
	def rotate(self,angl):
		self.angl += angl
		self.mg = pygame.transform.rotate(self.mg,-angl)
		print('rotating')
	def wait(self):
		keyboard.add_hotkey('w',lambda : self.eng())
		keyboard.add_hotkey('a',lambda : self.rotate(-90))
		keyboard.add_hotkey('d',lambda : self.rotate(90))
		



size = width, height = 1980, 1080
black = 255,255,255

screen = pygame.display.set_mode(size)

'''
ball1 = obect("intro_ball.gif", 30000,[0,-(10000*25/(10000))**0.5],800,500)
ball2 = obect("intro_ball.gif", 10000,[0,(30000*75/(10000))**0.5],700,500)
ball3 = obect("intro_ball.gif", 4000,[0,(675*(30000/490000+10000/360000))**0.5],100,500)
ball4 = obect("intro_ball.gif", 4000,[0,-(675*(30000/490000+10000/360000))**0.5],1400,500)

#rock = rocket("rock.png", 1,[0,0],100,500,1,1,0)
balls = [ball1,ball2,ball3,ball4]
#balls[4].wait()
'''

m = 500
ball1 = obect("intro_ball.gif", 10*m,[0,0],990,540)
ball2 = obect("intro_ball.gif", m+m//5,[0,(11.25*abs(m)/800)**0.5],190,540)
ball3 = obect("intro_ball.gif", m+m//500,[-(11.25*abs(m)/800)**0.5,0],990,-260)
ball4 = obect("intro_ball.gif", m+m//5,[0,-(11.25*abs(m)/800)**0.5],1790,540)
ball5 = obect("intro_ball.gif", m+m//500,[(11.25*abs(m)/800)**0.5,0],990,1340)

balls=obect_list([ball1,ball2,ball3,ball4,ball5])
'''
rock = rocket("rock.png", 0,[0,0],0,700,1,25,0)
rock.wait()
balls.append(rock)
'''
ms = sc(990,540,5)
ms.wait()
r = range(len(balls))
speeds = [[] for i in r]
p1,p2 = [],[]
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			
			fig = plt.figure()
			ev = fig.add_subplot(3,1,2)
			ev.grid('both')
			ev.set_title('all')
			s = [[]] * (r[-1]+1)
			for i in r:
				s[i] = fig.add_subplot(3,r[-1]+1,i+1)
				s[i].grid('both')
				s[i].set_title('ball' + str(i+1))
				s[i].plot(range(len(speeds[i])),speeds[i],'-')
				ev.plot(range(len(speeds[i])),speeds[i])
			imp = fig.add_subplot(3,2,5)
			imp.grid('both')
			imp.set_title('impuls1')
			imp.plot(range(len(p1)),p1)
			imp = fig.add_subplot(3,2,6)
			imp.grid('both')
			imp.set_title('impuls2')
			imp.plot(range(len(p2)),p2)
			plt.show()
		
	balls = balls.move()
	
	mc = obect.mass_center(balls)
	print(str(int(ms.n*100))+'%',ms.c)
	balls.react()
	
	p1.append(0)
	p2.append(0)
	for i in range(len(balls)):
		print(balls[i].m, balls[i].speed[2])
		speeds[i].append(balls[i].speed[2])
		p1[-1] += balls[i].m*balls[i].speed[0]
		p2[-1] += balls[i].m*balls[i].speed[1] 
	
	print()
	
	if ms.c == -1:
		xc = mc.x
		yc = mc.y
	elif ms.c == 0:
		xc = xc
		yc = yc
	else:
		ms.c = len(balls) if ms.c >= len(balls) else ms.c
		xc = balls[ms.c-1].x if ms.c - 1 < len(balls) else balls[r[-1]].x
		yc = balls[ms.c-1].y if ms.c - 1 < len(balls) else balls[r[-1]].y
		
	
	x = ms.n*ms.x - xc
	y = ms.n*ms.y - yc
	
	for ball in balls:
		ball = ball.move([x,y])

		
	
	screen.fill((255,150,200))
	for ball in balls:
		screen.blit(ball.mg, ball.rect)
	pygame.display.flip()
keyboard.wait()
