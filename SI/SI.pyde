add_library('minim')
import random 


def setup():
    global introimage, cannon, cannonx, score, game_state, alien, invasion
    size(700,750)
    introimage = loadImage('intro.jpg')
    cannon = loadImage('cannon.png')
    alien = loadImage('alien2.png')
    cannonx = (width/2)-(450/16)
    game_state = 0 
    score = 0 
    invasion = [[1 for x in range(11)] for i in range(5)]
    
    

def draw():
    intro()
    gameplay()





def gameplay(): 
    global game_state, cannon, cannonx, alien
    if game_state == 1:
        background(0,0,0)
        image(cannon, cannonx, 606.25, 450/8, 350/8)
        image(alien,0,0)
        
        
        

    
        
def intro():
    global game_state, introimage 
    if game_state == 0:
        image(introimage,0,0)
        
        
def keyPressed():
    global game_state, cannonx 
    if game_state == 0 and key == " ":
        game_state = 1
        
    if game_state == 1:
        if key == CODED:
            if keyCode == RIGHT and cannonx< (681-(450/8)):
                    cannonx += 20
            elif keyCode == LEFT and cannonx>19:
                cannonx -= 20
    
            
        
