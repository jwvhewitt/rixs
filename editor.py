# Level editor for RIXS

import pygame
import pygwrap
import maps
import image

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
                elif ev.key == pygame.K_ESCAPE:
                    keep_going = False

            elif ev.type == pygame.QUIT:
                keep_going = False



