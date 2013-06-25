import things
import player
import animob

class Item( things.Thing ):

    def update( self, levelmap ):
        # Items fall.
        if levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            # If we haven't reached terminal velocity yet, apply acceleration.
            if self.dy < self.TERMINAL_VELOCITY:
                self.dy += 1
        self.apply_dy( levelmap )

        # Check for encounters with the PC.
        for t in levelmap.contents:
            if isinstance( t , player.Player ) and self.is_touching( t ):
                self.interact( levelmap , t )

    def interact( self , levelmap , target ):
        levelmap.contents.remove( self )
        levelmap.contents.append( animob.YellowSparkle( self.mid_x() - 16 , self.mid_y() - 16 ))

class Potion( Item ):
    NAME = "Potion"

    def __init__( self , x , y ):
        super(Potion, self).__init__(x,y,width=22,height=22,sprite_name="bitz_heart.png",frame=2,topmargin=3,sidemargin=2,bottommargin=1)

    def interact( self , levelmap , target ):
        levelmap.contents.remove( self )
        levelmap.contents.append( animob.YellowSparkle( self.mid_x() - 16 , self.mid_y() - 16 ))
        target.potions += 1

class Heart( Item ):
    NAME = "Heart"

    def __init__( self , x , y ):
        super(Heart, self).__init__(x,y,width=22,height=22,sprite_name="bitz_heart.png",frame=0,topmargin=0,sidemargin=0,bottommargin=0)

    def interact( self , levelmap , target ):
        levelmap.contents.remove( self )
        levelmap.contents.append( animob.YellowSparkle( self.mid_x() - 16 , self.mid_y() - 16 ))
        target.health += 1
        target.full_health += 1


MANUAL = (Potion,Heart)
