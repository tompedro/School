import random as rnd
import os
import time
import pygame

DIRECTIONS = "w","a","s","d"
PATH = "./rooms"
background_colour = (0,0,0)
SCREEN_SIZE = (528, 480)
end = True

class Clock():
    def __init__(self,seconds):
        self.seconds = seconds
        self.p = 0
        self.start = time.time()
        self.t = 0
    def tick(self):
        self.t = time.time() - self.start
        if self.t - self.p > self.seconds + 0.5:
            self.p += self.seconds
            return False
        elif self.t - self.p >= self.seconds:
            self.p += self.seconds
            return True
        else:
            return False
    def restart(self):
        self.start = time.time()
        self.p = 0
        self.t = 0

class Game():
    def __init__(self,levels,n_lifes):
        
        pygame.init()
        self.font = pygame.font.SysFont("Arial",20)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0)

        self.ImagePath = [
        [pygame.image.load(".\\Resources\\Pavimenti\\Floor2.png"),
        pygame.image.load(".\\Resources\\Pavimenti\\Floor1.png"),
        pygame.image.load(".\\Resources\\Ostacoli\\Wall1.png"),
        pygame.image.load(".\\Resources\\Ostacoli\\Void.png")],
        [pygame.image.load(".\\Resources\\Personaggi\\player.png"),
        pygame.image.load(".\\Resources\\Personaggi\\Enemy.png")],
        [pygame.image.load(".\\Resources\\Ostacoli\\coin.png"),
        pygame.image.load(".\\Resources\\Ostacoli\\key.png"),
        pygame.image.load(".\\Resources\\Personaggi\\knife.png")]
        ]
        self.levels = levels
        self.currentLevelIndex = 0
        self.currentLevel = self.levels[self.currentLevelIndex]
        self.currentLevel.game = self

        pygame.display.set_caption("L'AVVENTURA DI MALARIO")
        
        self.score = 0
        self.win = False
        self.lose = False
        self.kills = 0
        self.life = n_lifes
        self.deads = 0
        self.bossLife = 3

    def dead(self):
        self.currentLevel.currentRoomIndex = 0
        self.currentLevel.currentRoom = self.currentLevel.rooms[self.currentLevel.currentRoomIndex]
        
        self.currentLevel.currentRoom.entities[0].level = self.currentLevel
        self.currentLevel.currentRoom.entities[0].x , self.currentLevel.currentRoom.entities[0].y = self.currentLevel.currentRoom.map[3][0][0],self.currentLevel.currentRoom.map[3][0][1]
    
    def Lose(self):
        os.system("cls")
        pygame.draw.rect(game.screen,(0,0,0),(0,0,*SCREEN_SIZE))
        game.screen.blit(game.font.render("GAME OVER, NOOB!",True,(255,255,0)),(180,240))
        pygame.display.flip()
        time.sleep(5)
        quit()

    def Win(self):
        if self.currentLevelIndex == len(self.levels) - 1:
            os.system("cls")
            pygame.draw.rect(game.screen,(0,0,0),(0,0,*SCREEN_SIZE))
            game.screen.blit(game.font.render("YOU WIN, FOR THIS TIME...",True,(255,255,0)),(180,240))
            game.screen.blit(game.font.render("(noob)",True,(255,255,0)),(220,270))
            pygame.display.flip()
            time.sleep(5)
            quit()
        else:
            self.currentLevelIndex += 1
            self.currentLevel = self.levels[self.currentLevelIndex]
            self.currentLevel.game = self

    

def getMap(path,level,room):
    contents = open ("{}.txt".format(path +"/"+str(level)+ "/" + str(room)), "r").readlines()
    for row in range(len(contents)):
        contents[row] = contents[row].replace(" ", "")
    r = [[],[],[],[],[],[],[],[],[]]
    for y in range(len(contents)):
        for x in range(len(contents[y])):
            char = contents[y][x]
            if char == "1":
                r[0].append((x,y))
            elif char == "£":
                r[1].append((x,y))
            elif char == "°":
                r[2].append((x,y))
            elif char == "2":
                r[3].append((x,y))
            elif char == "3":
                r[4].append((x,y))
            elif char == "4":
                r[5].append((x,y))
            elif char == "%":
                r[6].append((x,y))
            #boss
            elif char == "ç":
                r[7].append((x,y))
            elif char == "8":
                r[8].append((x,y))
    return r

class Entity():
    def __init__(self,x,y,graphic):
        self.level = None
        self.x = x
        self.y = y
        self.graphic = graphic
    def move(self,direction):
        futurex = self.x
        futurey = self.y
        if direction == DIRECTIONS[0]:
            if futurey > 0:
                futurey -= 1
            else:
                if isinstance(self,Knife) == False:
                    self.level.incrementCurrentRoom()
        elif direction == DIRECTIONS[1]:
            if futurex > 0:
                futurex -= 1
            else:
                if isinstance(self,Knife) == False:
                    self.level.incrementCurrentRoom()
            
        elif direction == DIRECTIONS[2]:
            if futurey < self.level.currentRoom.height - 1:
                futurey += 1
            else:
                if isinstance(self,Knife) == False:
                    self.level.incrementCurrentRoom()
            
        elif direction == DIRECTIONS[3]:
            if futurex < self.level.currentRoom.width - 1:
                futurex += 1
            else:
                if isinstance(self,Knife) == False:
                    self.level.incrementCurrentRoom()
            
            
        if self.level.getEntityAtCoords(futurex,futurey) == None:
            self.x,self.y = futurex,futurey
        else:
            if self.collide(self.level.getEntityAtCoords(futurex,futurey)) == True:
                self.x,self.y = futurex,futurey

    def collide(self , entity):
        pass
    def draw(self,x,y,i = None,j = None):
        self.level.game.screen.blit(self.level.game.ImagePath[i][j],(x * self.level.wide,y * self.level.wide + 60) , pygame.Rect(0,0,24,24))
        pass
    def update(self):
        pass


class Player(Entity):
    def __init__(self,x,y,graphic):
        super().__init__(x,y,graphic)
        self.throwed = False
        self.hack = False
    def collide(self,entity):
        if isinstance(entity,Enemy):
            if entity.lifes - 1 == 0:
                if isinstance(entity,Boss):
                    self.level.game.bossLifes = 0
                self.level.currentRoom.entities.remove(entity)
                self.level.game.kills += 1
                self.level.currentRoom.number_of_enemies -= 1
            else:
                entity.lifes -= 1
            return False
        elif isinstance(entity,Keys):
            if self.level.currentRoom.number_of_enemies == 0:
                self.level.currentRoom.entities.remove(entity)
                self.level.game.Win()
                return True
            else:
                return False
        elif isinstance(entity,Collectible):
            self.level.currentRoom.entities.remove(entity)
            self.level.game.score += 10
            return True
        elif isinstance(entity,Knife):
            if self.level.game.life <= 1:
                self.level.game.Lose()
            else:
                self.level.game.deads += 1
                self.level.game.life -= 1
                self.level.game.dead()
            return False
    def draw(self,x,y,i,j):
        super().draw(x,y,1,0)
    #insert def
    def throwKnifes(self):
        if self.throwed == False or self.hack == True:
            x = self.x
            y = self.y
            self.knifes = (Knife(x + 1,y,"d"),Knife(x - 1,y,"a"),Knife(x,y + 1,"s"),Knife(x, y - 1,"w"))
            for knife in self.knifes:
                knife.level = self.level
                self.level.currentRoom.entities.append(knife)
            self.throwed = True
    def update(self):
        if self.throwed == True:
            for knife in self.level.currentRoom.entities:
                if isinstance(knife,Knife):
                    knife.update()

class Obstacle(Entity):
    def draw(self,x,y,i,j):
        super().draw(x,y,i,j) 

class Floor(Entity):
    def draw(self,x,y,i,j):
        super().draw(x,y,0,3) 

class InvisibleObstacle(Obstacle):
    def __init__(self,x,y,graphic):
        super().__init__(x,y," ")
    def draw(self,x,y,i,j):
        super().draw(x,y,0,0)

class Enemy(Entity):
    def __init__(self,x,y,graphic):
        super().__init__(x,y,graphic)
        self.lifes = 1
        self.clock = Clock(0.5)
        self.count_movement = 0
        self.movements = []
    def collide(self,entity):
        if isinstance(entity,Player):
            if self.level.game.life <= 1:
                self.level.game.Lose()
            else:
                self.level.game.deads += 1
                self.level.game.life -= 1
                self.level.game.dead()
            return False
    def draw(self,x,y,i,j):
        super().draw(x,y,1,1)
    def FindPlayer(self,player):
        self.count_movement = 0
        movements = []
        if (self.x - player.x) < 0:
            movements.extend(["d"]*(-self.x+player.x))
        elif (self.x - player.x) > 0:
            movements.extend(["a"]*(self.x-player.x))
        if (self.y - player.y) < 0:
            movements.extend(["s"]*(player.y-self.y))
        elif (self.y - player.y) > 0:
            movements.extend(["w"]*(self.y-player.y))
        self.movements = movements
        
        return movements
    def update(self):
        if self.clock.tick() == True:
            if self.count_movement + 1 <= len(self.movements):
                self.move(self.movements[self.count_movement])
                self.count_movement += 1
class Boss(Enemy):
    def __init__(self,x,y,graphic):
        super().__init__(x,y,graphic)
        self.lifes = 3
        self.clockK = Clock(5)
        self.knifes = ()
    def update(self):
        self.level.game.bossLife = self.lifes
        x = self.x
        y = self.y
        super().update()
        if self.clockK.tick() == True:
            self.knifes = (Knife(x + 1,y,"d"),Knife(x - 1,y,"a"),Knife(x,y + 1,"s"),Knife(x, y - 1,"w"))
            for knife in self.knifes:
                knife.level = self.level
                self.level.currentRoom.entities.append(knife)
        
        if self.knifes != ():
            for knife in self.level.currentRoom.entities:
                if isinstance(knife,Knife):
                    knife.update()
class Collectible(Entity):
    def draw(self,x,y,i,j):
        if i == 0 and j == 2:
            super().draw(x,y,2,0)
        else:
            super().draw(x,y,i,j)

class Knife(Entity):
    def __init__(self,x,y,direction,graphic=","):
        super().__init__(x,y,",")
        self.Clock = Clock(0.1)
        self.direction = direction
    def draw(self,x,y,i,j):
        super().draw(x,y,2,2)
        pass
    def update(self):
        if self.Clock.tick() == True:
            self.move(self.direction)
    def collide(self,entity):
        if isinstance(entity,Player):
            if self.level.game.life <= 1:
                self.level.game.Lose()
            else:
                self.level.game.deads += 1
                self.level.game.life -= 1
                self.level.game.dead()
        elif isinstance(entity,Enemy):
            if entity.lifes - 1 == 0:
                self.level.currentRoom.entities.remove(entity)
                self.level.game.kills += 1
                self.level.currentRoom.number_of_enemies -= 1
            else:
                entity.lifes -= 1
        if self in self.level.currentRoom.entities:
            self.level.currentRoom.entities.remove(self)
        return False
class Keys(Collectible):
    def __init__(self,x,y,graphic):
        super().__init__(x,y,"$")
    def draw(self,x,y,i,j):
        super().draw(x,y,2,1)

    
class Level():
    def __init__(self,name,rooms):
        self.name = name
        self.rooms = rooms
        self.wide = 24
        
        self.game = None

        self.rooms[0].entities[0].level = self

        for room in self.rooms:
            room.name_of_level = name
            for entity in range(1,len(room.entities)):
                room.entities[entity].level  = self

        self.currentRoomIndex = 0
        self.currentRoom = self.rooms[self.currentRoomIndex]

        self.player_moves = self.currentRoom.getPlayer().x,self.currentRoom.getPlayer().y
        
    def update(self):
        self.draw()
        if self.currentRoom.number_of_enemies > 0:
            for enemy in self.currentRoom.entities:
                if isinstance(enemy,Enemy) or isinstance(enemy,Boss):
                    if self.player_moves != (self.currentRoom.getPlayer().x,self.currentRoom.getPlayer().y) or enemy.movements == []:
                        enemy.FindPlayer(self.currentRoom.getPlayer())
                    enemy.update()
        else:
            for wallInv in self.currentRoom.map[5]:
                for e in self.currentRoom.entities:
                    if e.x == wallInv[0] and e.y == wallInv[1]:
                        self.currentRoom.entities.remove(e)
            self.currentRoom.map[5].clear()
            

    def incrementCurrentRoom(self):
        if self.currentRoomIndex + 1 == len(self.rooms):
            self.game.Win()
            return
        self.currentRoomIndex += 1
        self.currentRoom = self.rooms[self.currentRoomIndex]
        self.currentRoom.entities[0].level = self.rooms[self.currentRoomIndex - 1].entities[0].level
        self.currentRoom.entities[0].throwed = False
        self.currentRoom.entities[0].x , self.currentRoom.entities[0].y = self.currentRoom.map[3][0][0],self.currentRoom.map[3][0][1]
        self.player_moves = self.currentRoom.getPlayer().x,self.currentRoom.getPlayer().y
        self.start = time.time()

    def draw(self):
        for y in range(self.currentRoom.height):
            for x in range(self.currentRoom.width):
                for e in self.currentRoom.entities:
                    if e.x == x and e.y == y:
                        #print("[{}]".format(e.graphic),end = "")
                        e.draw(x,y,0,2)
                        break
                else:
                    #print("[ ]",end = "")
                    self.game.screen.blit(self.game.ImagePath[0][0],(x * self.wide,y * self.wide + 60) , pygame.Rect(0,0,24,24))
            #print()

    def getEntityAtCoords(self,x,y):
        return self.currentRoom.getEntityAtCoords(x,y)


class Room():
    def __init__(self,number,name_of_level):
        self.number = number
        self.name_of_level = name_of_level
        map = getMap(PATH,self.name_of_level,self.number)
        self.map = map
        self.width = 22
        self.height = 17
        self.entities = []

        self.entities.append(Player(*map[3][0],"@"))
        self.number_of_enemies = 0

        for obstacle in map[0]:
            self.entities.append(Obstacle(*obstacle,"#"))
        for enemy in map[1]:
            self.entities.append(Enemy(*enemy,"£"))
            self.number_of_enemies += 1
        for collectible in map[2]:
            self.entities.append(Collectible(*collectible,"o"))
        for invisible in map[4]:
            self.entities.append(InvisibleObstacle(*invisible," "))
        for doors in map[5]:
            self.entities.append(Obstacle(*doors," "))
        for keys in map[6]:
            self.entities.append(Keys(*keys,"$"))
        for boss in map[7]:
            self.entities.append(Boss(*boss,"§"))
            self.number_of_enemies += 1
        for floor in map[8]:
            self.entities.append(Floor(*floor,"_"))
    def getEntityAtCoords(self,x,y):
        for e in self.entities:
            if e.x == x and e.y == y:
                return e
        
    def getPlayer(self):
        return self.entities[0]

level = Level(1,[Room(1,1),Room(2,1),Room(3,1),Room(4,1),Room(5,1),Room(6,1)])
game = Game([level],3)

clock = pygame.time.Clock()
hack = ""
while end:
    action = ""
    pygame.draw.rect(game.screen,(0,0,0),(0,0,SCREEN_SIZE[0],60))
    game.screen.blit(game.font.render("La tua score : " + str(game.score),True,(255,255,0)),(0,0))
    game.screen.blit(game.font.render("Le tue kills : " + str(game.kills),True,(255,255,0)),(0,15))
    game.screen.blit(game.font.render("Le tue vite : " + str(game.life),True,(255,255,0)),(200,0))
    game.screen.blit(game.font.render("Vite Boss : " + str(game.bossLife),True,(255,255,0)),(200,15))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_LEFT:
                action = "a"
            elif event.key == pygame.K_RIGHT:
                action  ="d"
            elif event.key == pygame.K_UP:
                action = "w"
            elif event.key == pygame.K_DOWN:
                action = "s"
            elif event.key == pygame.K_q:
                level.currentRoom.entities[0].throwKnifes()
            else:
                hack += pygame.key.name(event.key)

    if hack == "sosreturn":
        level.currentRoom.getPlayer().hack = True

    level.update()

    pygame.display.flip()
    level.currentRoom.entities[0].move(action)
    level.currentRoom.entities[0].update() 
    clock.tick(30)
    
