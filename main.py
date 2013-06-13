import pygame
import pygwrap
import maps
import player
import image
import monster
import rpgmenu
import backdrop

pygame.init()

# Set the screen size.
screen = pygame.display.set_mode((maps.SCREENWIDTH, maps.SCREENHEIGHT))
pygwrap.init()
rpgmenu.init()
pygame.display.set_caption( "~= RIXS =~" , "RIXS" )

TITLE_BG = backdrop.Backdrop( "bg_wests_rock5.png" )
TITLE_LOGO = image.Image( "logo.png" )
TITLE_COUNTER = 0

def predraw( screen ):
    global TITLE_COUNTER
    TITLE_BG.tile( screen , ( TITLE_COUNTER * 5 , TITLE_COUNTER ) )
    TITLE_LOGO.render( screen , ( 84 , 40 ) )
    TITLE_COUNTER += 5


mymenu = rpgmenu.Menu( screen , 150 , 280 , 340 , 170 )
mymenu.predraw = predraw

mymenu.add_item( "Play Game" , 1 )
mymenu.add_item( "Quit" , -1 )

keep_going = True

while keep_going:

    n = mymenu.query()

    if n == 1:
        the_level = maps.Map(width=25,height=16)
        pc = player.Player( x = 100, y=360 )
        # Start the player with a bit of bounce...
        pc.dy = -10
        the_level.contents.append( pc )

        bear = monster.AcidDragon( x= 170, y=200 )
        the_level.contents.append( bear )

        bear = monster.Frog( x= 350, y=240 )
        the_level.contents.append( bear )

        bat = monster.Bat( x= 500, y=100 )
        the_level.contents.append( bat )

        slime = monster.BlueSlime( x= 320, y=100 )
        the_level.contents.append( slime )

        the_level.play( pc , screen )

    elif n == -1:
        keep_going = False

    if pygwrap.GOT_QUIT:
        keep_going = False



