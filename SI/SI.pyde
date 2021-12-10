add_library('minim')
import random 


def setup():
    global bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    size(700,750)
    introimage = loadImage('intro.jpg')
    cannon = loadImage('cannon.png')
    alien = loadImage('alien2.png')
    alien.resize(30, 0)
    cannonx = (width/2)-(450/16)
    game_state = 0 
    score = 0 
    invasion = [[1 for x in range(11)] for i in range(5)]
    alienx = 100
    alieny = 50
    
    alienvx = 1
    alienvy = 40
    
    laserShot = False
    
    bullety = 0
    
    
    
    

def draw():
    intro()
    gameplay()



def gameplay(): 
    global bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    if game_state == 1:
        background(0,0,0)
        image(cannon, cannonx, 606.25, 450/8, 350/8)
        #image(alien,0,0)
        spawnAliens()
        
        if laserShot:
            cbullet()


def spawnAliens():
    global bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    
    # generate aliens
    for row in range(len(invasion[0])):
        for col in range(len(invasion)):
            if invasion[col][row] == 1:
                image(alien, alienx + row * 50, alieny + col * 40)
                
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
    global bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    if game_state == 0:
        image(introimage,0,0)

def cbullet():
    global bulletx, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    rect(bulletx, 606.25 - bullety, 5, 15) 
    bullety += 5
    
    if bullety > 500:
        bullety = 0
        laserShot = False
        
def keyPressed():
    global bulletx, bullety, laserShot, alienvx, alienvy, alienx, alieny, introimage, cannon, cannonx, score, game_state, alien, invasion
    if game_state == 0 and key == "s":
        game_state = 1

    if game_state == 1:
        if key == CODED:
            if keyCode == RIGHT and cannonx< (681-(450/8)):
                    cannonx += 20
            elif keyCode == LEFT and cannonx>19:
                cannonx -= 20
                
        if key == ' ':
            laserShot = True
            bulletx = cannonx

            
    
            
        
