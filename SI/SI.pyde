#testing branches
hitnum = 0
add_library('minim')
import random 

def setup():
    global won, endimagew ,endimagel, numPlayerLives, abulletdelay, adelaylen, abulletpos, bulletdelay, delaylen, myFont, cbulletpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, num, introsong, roundsong, endsong, winsong, music_state, shootsound

    size(700,750)
    
    minim = Minim(this)
    introsong = minim.loadFile('intro.mp3')
    roundsong = minim.loadFile('round.mp3')
    endsong = minim.loadFile('gameover.mp3')
    winsong = minim.loadFile('gamewon.mp3')
    shootsound = minim.loadFile('shoot.wav')
    
    myFont = createFont("si.ttf", 16)
    
    # images -----------------
    endimagew = loadImage('siendw.png')
    endimagel = loadImage('siendl.png')
    won = None

    introimage = loadImage('intro.jpg')
    cannon = loadImage('cannon.png')
    alien = loadImage('alien2.png')
    alien.resize(30, 0)
    cannonx = 0
    
    # game state variable -----------
    game_state = 0
    
    # alien spawn variables -----------
    invasion = [[1 for x in range(11)] for i in range(5)]
    
    alienx = 70
    alieny = 125
    
    alienvx = 1
    alienvy = 10
    
    # player bullet variables -------------------
    # stores x position and y increment (actual bullet pos found with 606.25 - y) of each bullet as a list inside cbulletpos list
    cbulletpos = []
    
    # stores how long has passed since user shot the last laser
    bulletdelay = 2
    
    # stores the delay length between bullets
    delaylen = bulletdelay - 1
    
    # alien bullet variables -------------------
    
    #stores x position and y position of alien bullet
    abulletpos = []

    abulletdelay = 100
    adelaylen = abulletdelay - 1 
    
    # life counter variables -----------
    numPlayerLives = 3
    
    # ---------
    left = False
    right = False
    
    num = 0
    music_state = 0
    score = 0
    

def draw():
    intro()
    gameplay()
    endscreen()
    '''music()'''
    


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
    global hitnum, abulletdelay, adelaylen, abulletpos, bulletdelay, delaylen, myFont, cbulletpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, num, introsong, roundsong, endsong, winsong, music_state, shootsound
    if game_state == 1:
        background(0,0,0)
        image(cannon, cannonx, 606.25, 450/8, 350/8) #resizes cannon to one eight its orignal size and places it at the right spot 
    
        spawnAliens()
        movealiens()
        sm()
        scoreboard()
        checkforend()
        
        for i in range(len(cbulletpos)):
            # cbullet takes 2 args: x pos and y incr of bullet
            # generates a bullet with that position
            cbullet(cbulletpos[i][0], cbulletpos[i][1])
            cbulletpos[i][1] += 8        
        
        
        # uses list comprehension to create a new list with bullets
        # that have a y position less than 606.25
        # basically just gets rid of bullets that are out of bounds
        
        cbulletpos = [ pos for pos in cbulletpos if pos[1] < 606.25 ]
        
        # checks if enough time has passed for the player to shoot another bullet
        if bulletdelay <= delaylen:
            bulletdelay += 1
                 
        # checks if enough time has passed for another alien to shoot a bullet
        if abulletdelay >= adelaylen:
            abulletdelay = 0
            whichAlienShoots()
            
        abulletdelay += 1
        
        
        for i in range(len(abulletpos)):
            # draws all alien bullets
            # xpos of bullet: abulletpos[i][0]
            # ypos of bullet: abulletpos[i][1]
            
            abullet(abulletpos[i][0], abulletpos[i][1])
            
            # increments ypos of bullet
            abulletpos[i][1] += 2
            
            
            # checks if an alien bullet has hit the player
            if (abulletpos[i][0]  >= cannonx ) and (abulletpos[i][0] + 2 <= cannonx + 450/8) and (abulletpos[i][1] >= 606.25 + 10 ):
                
                # move the bullet out of the screen if it has hit
                abulletpos[i][1] = 1000
                # hitnum +=1
                # print("hit {} times".format(hitnum))

            
        # despawn all bullets which are out of bounds
        abulletpos = [ pos for pos in abulletpos if pos[1] < 650.25 + 350/8 ]
        
        # delay length between alien bullets changes based on how close 
        # the aliens are to the bottom of the screen
        adelaylen = (606.25-alieny)/5
    
# randomly chooses an alien to shoot a bullet
# only aliens that are the bottom of each column can shoot a bullet
def whichAlienShoots():
    global abulletdelay, adelaylen, abulletpos, bulletdelay, delaylen, myFont, cbulletpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, num, introsong, roundsong, endsong, winsong, music_state, shootsound

    # create list with the indices of the aliens in the lowermost row of each column
    exposedAliens = []
    
    # create a list to find the last occurence of 1 in each column 
    colAliens = []
    
    # check which aliens are the lowermost
    for col in range(len(invasion[0])):
        for row in range(len(invasion)):
            colAliens.append(invasion[row][col])
            
        if 1 in colAliens:
            bottomAlien = [len(colAliens) - 1 - colAliens[::-1].index(1), col]
            exposedAliens.append(bottomAlien)
            
        colAliens = []
    
    # randomly chooses an alien to shoot
    activeAlien = random.choice(exposedAliens)
    
    # add initial xpos and ypos of new bullet in alien bullet list
    # initial xpos and ypos calculated based on the position of the alien in the invasion list
    abulletpos.append([alienx + activeAlien[1] * 50 + 15, alieny + activeAlien[0] * 40 + 22.4])

# draws an alien bullet
def abullet(x, y):
    global abulletdelay, adelaylen, abulletpos, bulletdelay, delaylen, myFont, cbulletpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, num, introsong, roundsong, endsong, winsong, music_state, shootsound
    fill(255)
    stroke(255)
    rect(x - 2.5, y, 2, 10)     


def isPlayerHit():
    #runs if bullet past a certain threshhold
    pass

def movealiens():
    global cbulletpos, bullety, bulletx, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, score 
    

    for row in range(len(invasion[0])):
        for col in range(len(invasion)):
            
            if invasion[col][row] == 1:
                if alienx+row*50 + 30 > width:
                    alienvx *= -1
                    alieny += alienvy
                    break
            
            
                if alienx+row*50 < 0:
                    alienvx *= -1
                    alieny += alienvy
                    break
                    
                if alieny + col * 40 + 22.4 > 606.25:
                    alienvy = 0
        
def checkforend():
    global game_state, invasion, alieny, alienvy, score, won
    if game_state == 1:
        for row in range(len(invasion[0])):
            for col in range(len(invasion)):
                if invasion[col][row] == 1:
                    if alieny + col * 40 + 22.4 > 606.25:
                        alienvy = 0
                        game_state = 2 
                        won = False
        if score == 550:
            game_state = 2
            won = True
        
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
    global cbulletpos, bullety, bulletx, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, score 
    
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
                
                #cbulletpos[i][1] is the y increment of the bullet in index i
                #cbulletpos[i][0] is the x value of the bullet in index i
                
                for i in range(len(cbulletpos)):
                    if ((606.25 - cbulletpos[i][1] < (alieny+col * 40)) and (606.25 - cbulletpos[i][1] > (alieny+col * 40 - 22.4))) and ((cbulletpos[i][0] - 2.5 > alienx + row * 50 and cbulletpos[i][0] -2.5 < alienx + row * 50+30) or (cbulletpos[i][0] + 2.5 > alienx + row * 50 and cbulletpos[i][0] + 2.5 < alienx + row * 50+30)) :
                   
                        
                        # despawns bullet that hit an alien
                        cbulletpos[i][1] = 900
                        
                        # in order to circumvent an index out of range error, 
                        # i basically just set the y position to a stupid big number
                        # so that it isnt in the screen, but on line 96
                        # i get rid of the bullet that hit the alien 
                        # the solution is dumb help me figure out a better one if u can

                        laserShot = False 
                        invasion[col][row] = 0 
                        score += 10#change to correct amount 
    alienx += alienvx
           
    
        
def intro():
    global bulletypos, bulletxpos, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    if game_state == 0:
        image(introimage,0,0)

def scoreboard():
    global score, myFont
    textFont(myFont)
    textSize(25)
    textAlign(LEFT)
    text("Score: %i" %(score), 60, 80)

    

def cbullet(x, y):
    global bulletdelay, delaylen, cbulletpos, bulletx, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    fill(255)
    stroke(255)
    rect(x, 606.25 - y, 5, 15) 
    
def endscreen(): 
    global game_state, endimagel,endimagew, won
    if game_state == 2:
        
        if won == True:
            image(endimagew,0,0)

        else:
            image(endimagel,0,0)
            
def keyPressed():
    global bulletdelay, delaylen, cbulletpos, bulletx, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion, left, right, music_state, shootsound
    
    if game_state == 0 and key == "s":
        game_state = 1
        music_state = 0 

    if game_state == 1:
        if key == CODED:
            if keyCode == RIGHT and cannonx< (681-(450/8)) and left == False:
                right = True
            elif keyCode == LEFT and cannonx>19 and right == False:
                left = True 
                
        if key == ' ' and bulletdelay > delaylen:
            # laserShot = True
            # bulletx = cannonx+28.125
            cbulletpos.append([cannonx+28.125, 0])
            bulletdelay = 0 
            #trying to implement time buffer between each bullet shot, so player
            # does not spam lasers
            #print(cbulletpos)
            
            #shootsound.play()
