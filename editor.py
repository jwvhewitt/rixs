# Level editor for RIXS

import maps

def edit_map( levelmap , screen ):
    # Edit this map in place.

    curs_x = 0
    curs_y = 0

    keep_going = True

    while keep_going:
            ev = pygwrap.wait_event()

            if ev.type == pygwrap.TIMEREVENT:
                levelmap.center_on( x * levelmap.tile_size , y * levelmap.tile_size )
                self.render( screen )
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
                    keep_going = False

            elif ev.type == pygame.QUIT:
                keep_going = False



