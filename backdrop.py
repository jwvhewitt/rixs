import image

class Backdrop( image.Image ):

    def tile( self , screen , dest , frame = 0 ):
        x0,y0 = dest
        start_x = ( -x0/ 10 ) % self.frame_width - self.frame_width
        start_y = ( -y0/ 10 ) % self.frame_height - self.frame_height

        for x in range( 0 , screen.get_width() / self.frame_width + 2 ):
            for y in range( 0 , screen.get_height() / self.frame_height + 2 ):
                self.render( screen , (x * self.frame_width + start_x , y * self.frame_height + start_y ) , frame )




