import random
import image
import pygame
import pygwrap
import backdrop

SCREENWIDTH = 640
SCREENHEIGHT = 480

LEFTMARGIN = 200
RIGHTMARGIN = SCREENWIDTH - LEFTMARGIN
TOPMARGIN = 200
BOTTOMMARGIN = SCREENHEIGHT - 200


def set_offset( levelmap , pc ):
    dx = pc.x - levelmap.off_x
    dy = pc.y - levelmap.off_y

    if dx < LEFTMARGIN:
        levelmap.off_x = pc.x - LEFTMARGIN
    elif dx > RIGHTMARGIN:
        levelmap.off_x = pc.x - RIGHTMARGIN
    if levelmap.off_x < 0:
        levelmap.off_x = 0
    elif levelmap.off_x > ( levelmap.width * levelmap.tile_size - SCREENWIDTH ):
        levelmap.off_x = levelmap.width * levelmap.tile_size - SCREENWIDTH

    if dy < TOPMARGIN:
        levelmap.off_y = pc.y - TOPMARGIN
    elif dy > BOTTOMMARGIN:
        levelmap.off_y = pc.y - BOTTOMMARGIN
    if levelmap.off_y < 0:
        levelmap.off_y = 0
    elif levelmap.off_y > ( levelmap.height * levelmap.tile_size - SCREENHEIGHT ):
        levelmap.off_y = levelmap.height * levelmap.tile_size - SCREENHEIGHT


class Map( object ):
    SPACE,OBSTACLE,PLATFORM = range(3)

    TERRAIN_TYPE = [ OBSTACLE, PLATFORM, SPACE ]

    def __init__(self,width=20,height=14,tile_size=32,sprite_name="default_terrain.png"):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.contents = []
        self.off_x = 0
        self.off_y = 0

        # Fill the map with empty tiles
        self.map = [[ -1
            for y in range(height) ]
                for x in range(width) ]
        self.sprite = image.Image( sprite_name , tile_size , tile_size )

        self.fill_terrain( 0 , 0 , height - 2 , width , 2 )
        self.fill_terrain( 1 , 5 , height - 4 , 10 , 1 )
        self.map[3][height - 3] = 2
        self.map[0][height - 3] = 0
        self.map[0][height - 4] = 0

        self.fill_terrain( 0 , 8 , height - 6 , 6 , 1 )
        self.fill_terrain( 0 , 15 , height - 7 , 5 , 2 )
        self.fill_terrain( 1 , 9 , height - 8 , 4 , 1 )

        self.backdrop = backdrop.Backdrop( "bg_longsunset.png" )

    def on_the_map( self , x , y ):
        # Returns true if on the map, false otherwise
        return ( ( x >= 0 ) and ( x < self.width ) and ( y >= 0 ) and ( y < self.height ) )

    def fill_terrain( self , terr , x1, y1, width, height ):
        # Fill this section of the map with terrain.
        for y in range(y1,y1+height):
            for x in range(x1,x1+width):
                if self.on_the_map(x,y):
                    self.map[x][y] = terr

    def render(self,screen):
        self.backdrop.tile( screen , (self.off_x,self.off_y) )
        screen_area = screen.get_rect()
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x][y] > -1:
                    dest = pygame.Rect( x*self.tile_size-self.off_x , y*self.tile_size-self.off_y , self.tile_size , self.tile_size )
                    if screen_area.colliderect( dest ):
                        self.sprite.render( screen , dest, self.map[x][y] )
        for t in self.contents:
            t.render( screen , self )

    def update( self ):
        for t in self.contents:
            t.update( self )

    def tile_x( self, screen_x ):
		if screen_x > 0:
			return int( screen_x / self.tile_size )
		else:
			return -1

    def tile_y( self, screen_y ):
		if screen_y > 0:
			return int( screen_y / self.tile_size )
		else:
			return -1

    def center_on( self , screen_x , screen_y ):
        # Center the display on the requested point.
        self.off_x = screen_x - SCREENWIDTH / 2
        self.off_y = screen_y - SCREENHEIGHT / 2

    def is_an_obstacle( self , screen_x , screen_y ):
        tile_x = self.tile_x( screen_x )
        tile_y = self.tile_y( screen_y )
        if self.on_the_map( tile_x , tile_y ):
            return self.TERRAIN_TYPE[ self.map[tile_x][tile_y] ] == self.OBSTACLE
        else:
            return True

    def is_a_space( self , screen_x , screen_y ):
        tile_x = self.tile_x( screen_x )
        tile_y = self.tile_y( screen_y )
        if self.on_the_map( tile_x , tile_y ):
            return self.TERRAIN_TYPE[ self.map[tile_x][tile_y] ] == self.SPACE
        else:
            return True

    def is_a_platform( self , screen_x , screen_y ):
        tile_x = self.tile_x( screen_x )
        tile_y = self.tile_y( screen_y )
        if self.on_the_map( tile_x , tile_y ):
            return self.TERRAIN_TYPE[ self.map[tile_x][tile_y] ] == self.PLATFORM
        else:
            return True

    def play( self , pc , screen ):
        keep_playing = True
        while keep_playing:
            # Get some input...
            ev = pygwrap.wait_event()

            if ev.type == pygwrap.TIMEREVENT:
                self.update()

                set_offset( self , pc )

                self.render( screen )
                pc.render_health( screen )
                pygame.display.flip()

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    pc.move_up = True
                elif ev.key == pygame.K_LEFT:
                    pc.move_left = True
                elif ev.key == pygame.K_RIGHT:
                    pc.move_right = True
                elif ev.key == pygame.K_SPACE:
                    pc.fire_button = True
                elif ev.key == pygame.K_ESCAPE:
                    keep_playing = False

            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_UP:
                    pc.move_up = False
                elif ev.key == pygame.K_LEFT:
                    pc.move_left = False
                elif ev.key == pygame.K_RIGHT:
                    pc.move_right = False
                elif ev.key == pygame.K_SPACE:
                    pc.fire_button = False

            elif ev.type == pygame.QUIT:
                keep_playing = False


