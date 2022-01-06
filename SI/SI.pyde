add_library('minim')
import random 

def setup():
    global bulletbuffer, bulletpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, num, introsong, roundsong, endsong, winsong, music_state, shootsound
    size(700,750)
    minim = Minim(this)
    introsong = minim.loadFile('intro.mp3')
    roundsong = minim.loadFile('round.mp3')
    endsong = minim.loadFile('gameover.mp3')
    winsong = minim.loadFile('gamewon.mp3')
    shootsound = minim.loadFile('shoot.wav')
    
    
    introimage = loadImage('intro.jpg')
    cannon = loadImage('cannon.png')
    alien = loadImage('alien2.png')
    alien.resize(30, 0)
    cannonx = 0
    #321.875 # middle of screen
    
    game_state = 0
    score = 0 
    invasion = [[1 for x in range(11)] for i in range(5)]
    alienx = 100
    alieny = 50
    
    alienvx = 1
    alienvy = 10
    
    laserShot = False

    bullety = 0
    
    # stores x position and y increment (actual bullet pos found with 606.25 - y) of each bullet as a list inside bulletpos list
    bulletpos = []

    
    left = False
    right = False
    num = 0
    music_state = 0
    score = 0
    

def draw():
    intro()
    gameplay()
    music()
    


def music():
    global music_state, game_state
    
    if music_state == 0:
        if introsong.isPlaying():
            introsong.pause()
            introsong.rewind()
        elif roundsong.isPlaying():
            roundsong.pause()
            roundsong.rewind()
        elif endsong.isPlaying():
            endsong.pause()
            endsong.rewind()
        elif winsong.isPlaying():
            winsong.pause()
            winsong.rewind()
        
            
    
    if game_state == 0 and music_state == 0:
        introsong.loop()
        music_state = 1
    if game_state == 1 and music_state == 0:
        roundsong.loop()
        music_state = 1 
        

def gameplay(): 
    global bulletbuffer, bulletpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    if game_state == 1:
        background(0,0,0)
        image(cannon, cannonx, 606.25, 450/8, 350/8) #resizes cannon to one eight its orignal size and places it at the right spot 
        image(alien,0,0)
        spawnAliens()
        sm()
        
    for i in range(len(bulletpos)):
        # changed cbullet() in to a function that takes 2 args: x pos and y incr of bullet
        # generates a bullet with that position
        cbullet(bulletpos[i][0], bulletpos[i][1])
        bulletpos[i][1] += 8        
    
    
    # basically, i use list comprehension to create a new list with bullets
    # that have a y increment less than 606.25
    # basically just gets rid of bullets that are out of bounds
    bulletpos = [ pos for pos in bulletpos if pos[1] < 606.25 ]


def sm(): 
    global left, right, game_state, num, cannonx
    
    if left:
        cannonx -= 5 
        num += 5
    
    if right:
        cannonx += 5 
        num += 5 
        
        
    if num == 20:
        num = 0 
        left = False 
        right = False

def spawnAliens():
    global bulletpos, bullety, bulletx, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, score 
    
    # generate aliens
    for row in range(len(invasion[0])):
        for col in range(len(invasion)):
            if invasion[col][row] == 1:
                image(alien, alienx + row * 50, alieny + col * 40)
                
                #draw hitboxes
                noFill()
                stroke(102,255,0)
                rect(alienx+row*50, alieny+col * 40, 30,22.4)
                #checks for overlap of each bullet every frame
                
                #bulletpos[i][1] is the y increment of the bullet in index i
                #bulletpos[i][0] is the x value of the bullet in index i
                
                for i in range(len(bulletpos)):
                    if ((606.25 - bulletpos[i][1] < (alieny+col * 40)) and (606.25 - bulletpos[i][1] > (alieny+col * 40 - 22.4))) and ((bulletpos[i][0] - 2.5 > alienx + row * 50 and bulletpos[i][0] -2.5 < alienx + row * 50+30) or (bulletpos[i][0] + 2.5 > alienx + row * 50 and bulletpos[i][0] + 2.5 < alienx + row * 50+30)) :
                        print("true")
                        
                        # despawns bullet that hit an alien
                        bulletpos[i][1] = 900
                        
                        # in order to circumvent an index out of range error, 
                        # i basically just set the y position to a stupid big number
                        # so that it isnt in the screen, but on line 96
                        # i get rid of the bullet that hit the alien 
                        # the solution is dumb help me figure out a better one if u can

                        laserShot = False 
                        invasion[col][row] = 0 
                        score += 10#change to correct amount 
                
                
                        
                          
    
                
                
                
                
                
                
                
                
    # change alien movement
    alienx += alienvx
    
    if alienx + 530 > width:
        alienvx *= -1
        alieny += alienvy


    if alienx < 0:
        alienvx *= -1
        alieny += alienvy
        
    if alieny > 606.25 - 40*5:
        alienvy = 0

    
            
    
        
def intro():
    global bulletypos, bulletxpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    if game_state == 0:
        image(introimage,0,0)

def cbullet(x, y):
    global bulletbuffer, bulletpos, bulletx, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    fill(255)
    stroke(255)
    rect(x - 2.5, 606.25 - y, 5, 15) 
    bullety += 8
    
        
        
def keyPressed():
    global bulletbuffer, bulletpos, bulletx, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, music_state, shootsound
    
    if game_state == 0 and key == "s":
        game_state = 1
        music_state = 0 

    if game_state == 1:
        if key == CODED:
            if keyCode == RIGHT and cannonx< (681-(450/8)) and left == False:
                    right = True
            elif keyCode == LEFT and cannonx>19 and right == False:
                left = True 
                
        if key == ' ':
            # laserShot = True
            # bulletx = cannonx+28.125
            bulletpos.append([cannonx+28.125, 0])
            #bulletbuffer = 0 
            #trying to implement time buffer between each bullet shot, so player
            # does not spam lasers
            print(bulletpos)
            
            shootsound.play()
  
            
    
            
        
