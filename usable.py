import things
import player
import animob

class Usable( things.Thing ):
    counter = 0

    def update( self, levelmap ):
        # Usables fall.
        if levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            # If we haven't reached terminal velocity yet, apply acceleration.
            if self.dy < self.TERMINAL_VELOCITY:
                self.dy += 1
        self.apply_dy( levelmap )

        if self.counter > 0:
            self.counter += -1

        # Check for encounters with the PC.
        for t in levelmap.contents:
            if isinstance( t , player.Player ) and self.is_touching( t ):
                # To use a usable, the player must be pressing "down".
                if t.move_down:
                    self.interact( levelmap , t )
                elif self.counter == 0:
                    # If the PC has just moved into contact with this usable,
                    # show that it's usable.
                    levelmap.contents.append( animob.DownArrow( self.mid_x() - 16 , self.mid_y() - 48 ))
                    self.counter = 300

    def interact( self , levelmap , target ):
        pass

class Fountain( Usable ):
    NAME = "Fountain"

    def __init__( self , x , y ):
        super(Fountain, self).__init__(x,y,width=32,height=32,sprite_name="usable_misc.png",frame=0,topmargin=3,sidemargin=2,bottommargin=1)

    def interact( self , levelmap , target ):
        target.health = target.full_health
        levelmap.contents.append( animob.Twinkle( target.mid_x() - 16 , target.mid_y() - 16 ))

class ArmorUp( Usable ):
    NAME = "ArmorUp"
    ready = True

    def __init__( self , x , y ):
        super(ArmorUp, self).__init__(x,y,width=32,height=32,sprite_name="usable_misc.png",frame=1,topmargin=3,sidemargin=2,bottommargin=1)

    def interact( self , levelmap , target ):
        if self.ready:
            target.armor += 1
            levelmap.contents.append( animob.EquipUp( self.mid_x() - 16 , self.mid_y() - 16 , frame=target.armor ))
            self.ready = False
            self.frame = 2
            self.counter = -1



MANUAL = ( Fountain , ArmorUp )
