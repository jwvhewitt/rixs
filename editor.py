# Level editor for RIXS

import pygame
import pygwrap
import maps
import image
import rpgmenu
import os.path
import pickle
import player
import monster
import copy
import generator
import items
import usable


TERRAIN_NEXT = {0:1,1:2,2:3,3:0,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12,12:4,15:16,16:17,17:18,50:51,51:52,52:53,53:50,54:55,55:56,56:54}


class MenuRedrawer( object ):
    def __init__( self , caption , screen , backdrop = "bg_kde_fractalnebula.jpg", levelmap = None ):
        self.caption = caption
        self.backdrop = image.Image( backdrop )
        self.counter = 0
        self.levelmap = levelmap

        self.rect = pygame.Rect( screen.get_width()/2 - 200 , screen.get_height()/2 - 220, 400, 64 )

    def __call__( self , screen ):
        if self.levelmap != None:
            self.levelmap.render( screen , show_special = True )
        else:
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

def choose_terrain( levelmap , screen ):
    # Instead of going back and forth, just pick a terrain from the sprite image.
    keep_going = True

    myrect = levelmap.sprite.bitmap.get_rect( center = ( screen.get_width() / 2 , screen.get_height() / 2 ) )
    terrain = -1

    while keep_going:
            ev = pygwrap.wait_event()

            if ev.type == pygwrap.TIMEREVENT:
                levelmap.render( screen , show_special = True )
                screen.blit( levelmap.sprite.bitmap , myrect )
                pygame.display.flip()

            elif ( ev.type == pygame.MOUSEBUTTONDOWN ) and myrect.collidepoint( ev.pos ):
                x,y = ev.pos
                x -= myrect.left
                y -= myrect.top

                terrain = x / levelmap.tile_size + ( y / levelmap.tile_size ) * 10

                keep_going = False

            elif ( ev.type == pygame.KEYDOWN ) and ( ev.key == pygame.K_ESCAPE ):
                keep_going = False

    return terrain



def select_monster( levelmap , screen , prompt = "Select a Monster" ):
    # Bring up a menu to select a monster, then return its class.
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    for m in monster.MANUAL:
        rpm.add_item( m.NAME , m )
    rpm.sort()
    myredraw = MenuRedrawer( prompt , screen , levelmap = levelmap )
    rpm.predraw = myredraw
    return rpm.query()

def select_item( levelmap , screen , prompt = "Select an Item" ):
    # Bring up a menu to select a monster, then return its class.
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    for m in items.MANUAL:
        rpm.add_item( m.NAME , m )
    rpm.sort()
    myredraw = MenuRedrawer( prompt , screen , levelmap = levelmap )
    rpm.predraw = myredraw
    return rpm.query()

def select_usable( levelmap , screen , prompt = "Select a Usable" ):
    # Bring up a menu to select a monster, then return its class.
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    for m in usable.MANUAL:
        rpm.add_item( m.NAME , m )
    rpm.sort()
    myredraw = MenuRedrawer( prompt , screen , levelmap = levelmap )
    rpm.predraw = myredraw
    return rpm.query()

def select_number( levelmap , screen , a , b, c, prompt = "Select Number of Products" ):
    # Select a number for whatever reason. a,b,c are the input for range.
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    for t in range( a , b, c ):
        rpm.add_item( str( t ) , t )
    myredraw = MenuRedrawer( prompt , screen , levelmap = levelmap )
    rpm.predraw = myredraw
    return rpm.query()

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
                levelmap.render( screen , show_special = True )
                edit_cursor.render( screen , ( screen.get_width() / 2 - 16 , screen.get_height() / 2 - 16 ) , 0 )
                pygwrap.draw_text( screen , pygwrap.SMALLFONT , str( curs_x ) + "," + str( curs_y ) + '  things:' + str( len( levelmap.contents ) ) , pygame.Rect( 8 , 42 , 256 , 32 ) )

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
                    if terrain in TERRAIN_NEXT:
                        terrain = TERRAIN_NEXT[ terrain ]

                elif ev.unicode == u"_":
                    for x in range( 0 , levelmap.width ):
                        levelmap.map[x][curs_y] = terrain
                        if terrain in TERRAIN_NEXT:
                            terrain = TERRAIN_NEXT[ terrain ]

                elif ev.key == pygame.K_DELETE:
                    # If there's a thing in this tile, delete it.
                    # If not, delete the map terrain.
                    deleted_thing = False
                    for t in levelmap.contents:
                        if ( t.x == curs_x * levelmap.tile_size ) and ( t.y == curs_y * levelmap.tile_size ):
                            levelmap.contents.remove( t )
                            deleted_thing = True
                    if not deleted_thing:
                        levelmap.map[curs_x][curs_y] = -1
                elif ev.key == pygame.K_b:
                    select_backdrop( levelmap , screen )
                elif ev.key == pygame.K_p:
                    levelmap.pc_start_x = curs_x
                    levelmap.pc_start_y = curs_y

                elif ev.key == pygame.K_F1:
                    lm2 = copy.deepcopy( levelmap )
                    pc = player.Player()
                    lm2.enter( pc , screen )

                elif ev.key == pygame.K_TAB:
                    terrain = choose_terrain( levelmap , screen )

                elif ev.key == pygame.K_m:
                    monster = select_monster( levelmap , screen )
                    if monster:
                        levelmap.contents.append( monster( x = curs_x * levelmap.tile_size , y = curs_y * levelmap.tile_size ) )

                elif ev.key == pygame.K_i:
                    item = select_item( levelmap , screen )
                    if item:
                        levelmap.contents.append( item( x = curs_x * levelmap.tile_size , y = curs_y * levelmap.tile_size ) )

                elif ev.key == pygame.K_u:
                    item = select_usable( levelmap , screen )
                    if item:
                        levelmap.contents.append( item( x = curs_x * levelmap.tile_size , y = curs_y * levelmap.tile_size ) )

                elif ev.key == pygame.K_g:
                    monster = select_monster( levelmap , screen , prompt = "Select Monster to Generate" )
                    n = select_number( levelmap , screen , 1, 11, 1, prompt = "How many at once?" )
                    freq = select_number( levelmap , screen , 30, 301 , 30, prompt = "How often to generate?" )
                    if monster and n:
                        levelmap.contents.append( generator.Generator(x = curs_x * levelmap.tile_size , y = curs_y * levelmap.tile_size, product=monster, number = n , frequency = freq ) )

                elif ev.key == pygame.K_s:
                    if levelmap.fname == "":
                        levelmap.fname = "gorch.dat"
                    f = open( "level/" + levelmap.fname , "wb" )
                    pickle.dump( levelmap , f , -1 )
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

def edit_existing_level( screen ):
    rpm = rpgmenu.Menu( screen , x=screen.get_width()/2 - 200 , y=screen.get_height()/2 - 130, w=400, h=300 )
    rpm.add_files( "level/*" )
    myredraw = MenuRedrawer( "Select Backdrop Image" , screen )
    rpm.predraw = myredraw
    pathname = rpm.query()
    if pathname:
        dname,fname = os.path.split( pathname )
        levelmap = maps.load( fname )
        edit_map( levelmap , screen )


