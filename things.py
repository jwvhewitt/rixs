import image
import pygame
import math


class Thing( object ):
    # A Thing is a generic game object, i.e. the parent class of just about
    # everything else.
    def __init__(self, x=0, y=0, width=32, height=32, sprite_name="", frame=0, topmargin=0, sidemargin=0, bottommargin=0 ):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height
        self.sprite_name = sprite_name
        self.sprite = None
        self.frame = frame
        self.topmargin = topmargin
        self.sidemargin = sidemargin
        self.bottommargin = bottommargin

    def liverect( self ):
        """ return the live rectangle to be used for collision detection, etc
        """
        return pygame.Rect( self.x + self.sidemargin, self.y + self.topmargin, self.width - 2 * self.sidemargin , self.height - self.topmargin - self.bottommargin )

    def is_touching( self , other ):
        """ Check whether this element is touching the other element.
        """
        r1 = self.liverect()
        r2 = other.liverect()
        return r1.colliderect( r2 )

    def update( self, levelmap ):
        pass

    def render( self, screen, levelmap ):
        if self.sprite == None:
            self.sprite = image.Image( self.sprite_name , self.width , self.height )
        self.sprite.render( screen , (self.x-levelmap.off_x,self.y-levelmap.off_y), self.frame )

    def decelerate_x( self ):
        if self.dx > 0:
            self.dx += -1
        elif self.dx < 0:
            self.dx += 1

    def apply_dy( self, levelmap ):
        # Returns True if the thing has just landed, False otherwise.
        has_just_landed = False
        self.y += self.dy
        if self.dy < 0:
            # Jumping up! Check the head for bumps.
            if levelmap.is_an_obstacle( self.head_x() , self.head_y() ):
                self.dy = 0
        elif self.dy > 0:
            # Falling down! Check for a landing.
            # Only do a landing check if the feet move from one tile to another.
            if levelmap.tile_y( self.foot_y() ) != levelmap.tile_y( self.foot_y() - self.dy ):
                if levelmap.is_an_obstacle( self.foot_x(), self.foot_y() ) or levelmap.is_a_platform( self.foot_x() , self.foot_y() ):
                    # We want to land exactly at the surface of the tile, not embedded part way through it.
                    # The following formula might be magic but it works.
                    self.y = ( self.y / levelmap.tile_size ) * levelmap.tile_size + levelmap.tile_size - ( ( self.height - self.bottommargin ) % levelmap.tile_size )
                    self.dy = 0
                    has_just_landed = True
        return has_just_landed

    def apply_dx( self, levelmap ):
        if not levelmap.is_an_obstacle(self.foot_x()+self.dx, self.foot_y()-1):
            self.x += self.dx

    def foot_x( self ):
        return self.x + int( self.width / 2 )

    def foot_y( self ):
        return self.y + self.height - self.bottommargin

    def head_x( self ):
        return self.x + int( self.width / 2 )

    def head_y( self ):
        return self.y + self.topmargin

    def mid_x( self ):
        return self.x + int( self.width / 2 )

    def mid_y( self ):
        return self.y + self.topmargin + int( ( self.height - self.topmargin - self.bottommargin ) / 2 )

class LivingThing( Thing ):
    # This is for living creatures of various kinds.
    def __init__(self, x=0, y=0, width=64, height=64, sprite_name="", frame=0, topmargin=0, sidemargin=0, bottommargin=0, health=1 ):
        super(LivingThing, self).__init__(x,y,width,height,sprite_name,frame,topmargin,sidemargin,bottommargin)
        self.health = health
        self.delay = 0
        self.shield = 0

    CAN_KNOCK_BACK = True
    AFTER_HIT_SHIELD_LENGTH = 10
    KNOCKBACK_LENGTH = 6
    KNOCKBACK_SPEED = 16
    TERMINAL_VELOCITY = 10

    def hurt( self, damage, source_rect, levelmap ):
        # This element has just been hurt by something located in source_rect.
        x,y = source_rect.center
        if self.shield == 0 and self.health > 0:
            self.health -= damage
            self.shield = self.AFTER_HIT_SHIELD_LENGTH
            self.hit( levelmap )
            if self.CAN_KNOCK_BACK:
                self.delay = self.KNOCKBACK_LENGTH
                self.dx = int( math.copysign( self.KNOCKBACK_SPEED , self.mid_x() - x ) )

    def hit( self , levelmap ):
        # This Thing has just been hit for damage. Do whatever you need to do.
        pass



