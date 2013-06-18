# Level editor for RIXS

import pygame
import pygwrap
import maps
import image
import rpgmenu
import os.path
import pickle

class MenuRedrawer( object ):
    def __init__( self , caption , screen ):
        self.caption = caption
        self.backdrop = image.Image( "bg_kde_fractalnebula.jpg" )
        self.counter = 0

        self.rect = pygame.Rect( screen.get_width()/2 - 200 , screen.get_height()/2 - 220, 400, 64 )

    def __call__( self , screen ):
        self.backdrop.tile( screen , ( self.counter * 5 , self.counter ) )
        pygwrap.draw_border( screen , self.rect )
        pygwrap.draw_text( screen , rpgmenu.MENUFONT , self.caption , self.rect , do_center = True )
        self.counter += 5


def select_backdrop( levelmap , screen ):
    # Select a backdrop from the ones on disk.
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    rpm.add_files( "gfx/bg_*.*" )

    myredraw = MenuRedrawer( "Select Backdrop Image" , screen )
    rpm.predraw = myredraw

    pathname = rpm.query()
    if pathname:
        dname,fname = os.path.split( pathname )
        levelmap.backdrop = image.Image( fname )

def edit_map( levelmap , screen ):
    # Edit this map in place.
    edit_cursor = image.Image( "edit_cursors.png" , 32 , 32 )

    curs_x = 0
    curs_y = 0

    terrain = -1

    keep_going = True

    while keep_going:
            ev = pygwrap.wait_event()

            if ev.type == pygwrap.TIMEREVENT:
                levelmap.center_on( curs_x * levelmap.tile_size + 16 , curs_y * levelmap.tile_size + 16 )
                levelmap.render( screen )
                edit_cursor.render( screen , ( screen.get_width() / 2 - 16 , screen.get_height() / 2 - 16 ) , 0 )

                if terrain > -1:
                    levelmap.sprite.render( screen , ( 8 , 8 ) , terrain )
                edit_cursor.render( screen , ( 8 , 8 ) , 1 )

                pygame.display.flip()

            elif ev.type == pygame.KEYDOWN:
                if ( ev.key == pygame.K_UP ) and ( curs_y > 0 ):
                    curs_y += -1
                elif ( ev.key == pygame.K_DOWN ) and ( curs_y < ( levelmap.height - 1 ) ):
                    curs_y += 1
                elif ( ev.key == pygame.K_LEFT ) and ( curs_x > 0 ):
                    curs_x += -1
                elif ( ev.key == pygame.K_RIGHT ) and ( curs_x < ( levelmap.width - 1 ) ):
                    curs_x += 1
                elif ev.key == pygame.K_LEFTBRACKET:
                    terrain += -1
                    if terrain < -1:
                        terrain = levelmap.sprite.num_frames() - 1
                elif ev.key == pygame.K_RIGHTBRACKET:
                    terrain += 1
                    if terrain >= levelmap.sprite.num_frames():
                        terrain = -1
                elif ev.key == pygame.K_SPACE:
                    levelmap.map[curs_x][curs_y] = terrain
                elif ev.key == pygame.K_DELETE:
                    levelmap.map[curs_x][curs_y] = -1
                elif ev.key == pygame.K_b:
                    select_backdrop( levelmap , screen )

                elif ev.key == pygame.K_s:
                    if levelmap.fname == "":
                        levelmap.fname = "gorch.dat"
                    f = open( "level/" + levelmap.fname , "w" )
                    pickle.dump( levelmap , f )
                    f.close()

                elif ev.key == pygame.K_ESCAPE:
                    keep_going = False

            elif ev.type == pygame.QUIT:
                keep_going = False

def create_new_level( screen ):
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    myredraw = MenuRedrawer( "Select Width" , screen )
    for t in range( 20 , 305 , 10 ):
        rpm.add_item( "Width: " + str( t ) , t )
    rpm.predraw = myredraw
    width = rpm.query()

    if width:
        rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
        for t in range( 20 , 205 , 10 ):
            rpm.add_item( "Height: " + str( t ) , t )
        myredraw.caption = "Select Height"
        rpm.predraw = myredraw
        height = rpm.query()

        if height:
            the_level = maps.Map(width=width,height=height)
            select_backdrop( the_level , screen )
            myredraw.caption = "Enter Filename"
            fname = pygwrap.input_string( screen, rpgmenu.MENUFONT, redrawer=myredraw, prompt="Enter Filename")
            the_level.fname = fname
            edit_map( the_level , screen )


