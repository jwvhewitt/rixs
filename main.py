#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
import pygwrap
import maps
import player
import image
import monster
import rpgmenu
import editor

pygame.init()

# Set the screen size.
screen = pygame.display.set_mode((maps.SCREENWIDTH, maps.SCREENHEIGHT))
pygwrap.init()
rpgmenu.init()
pygame.display.set_caption( "~= RIXS =~" , "RIXS" )

TITLE_BG = image.Image( "bg_wests_rock5.png" )
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
mymenu.add_item( "Create Level" , 2 )
mymenu.add_item( "Edit Level" , 3 )
mymenu.add_item( "Quit" , -1 )

keep_going = True

while keep_going:

    n = mymenu.query()

    if n == 1:
        the_level = maps.load( "gorch.dat" )
        pc = player.Player( x = 100, y=360 )
        the_level.enter( pc , screen )

    elif n == 2:
        editor.create_new_level( screen )

    elif n == 3:
        editor.edit_existing_level( screen )

    elif n == -1:
        keep_going = False

    if pygwrap.GOT_QUIT:
        keep_going = False



