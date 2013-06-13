# Load one image file, use it for multiple images.

import pygame

# Keep a list of already-loaded images, to save memory when multiple objects
# need to use the same image file.
pre_loaded_images = {}

class Image( object ):
    def __init__(self,fname,frame_width=0,frame_height=0):
        if fname in pre_loaded_images:
            self.bitmap = pre_loaded_images[fname]
        else:
            self.bitmap = pygame.image.load( "gfx/" + fname ).convert()
            self.bitmap.set_colorkey((0,0,255),pygame.RLEACCEL)
            pre_loaded_images[fname] = self.bitmap

        if frame_width == 0:
            frame_width = self.bitmap.get_width()
        if frame_height == 0:
            frame_height = self.bitmap.get_height()

        if frame_width > self.bitmap.get_width():
            frame_width = self.bitmap.get_width()
        self.fname = fname
        self.frame_width = frame_width
        self.frame_height = frame_height

    def render( self , screen , dest , frame = 0 ):
        # Render this Image onto the provided surface.
        # Start by determining the correct sub-area of the image.
        frames_per_row = self.bitmap.get_width() / self.frame_width
        area_x = ( frame % frames_per_row ) * self.frame_width
        area_y = ( frame / frames_per_row ) * self.frame_height
        area = pygame.Rect( area_x , area_y , self.frame_width , self.frame_height )
        screen.blit(self.bitmap , dest , area )

    def __reduce__( self ):
        # Rather than trying to save the bitmap image, just save the filename.
        return Image, ( self.fname , self.width , self.height )

if __name__ == '__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode((540, 960))

    myimg = Image( "image/sys_defborder.png" , 8 , 8 )

    screen.fill((0,0,0))
    myimg.render( screen , ( 10 , 10 ) , 0 )
    myimg.render( screen , ( 18 , 10 ) , 1 )
    myimg.render( screen , ( 10 , 18 ) , 2 )
    myimg.render( screen , ( 26 , 10 ) , 3 )
    myimg.render( screen , ( 26 , 18 ) , 2 )
    myimg.render( screen , ( 10 , 26 ) , 4 )
    myimg.render( screen , ( 18 , 26 ) , 1 )
    myimg.render( screen , ( 26 , 26 ) , 5 )

    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break



