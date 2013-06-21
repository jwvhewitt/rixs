import things
import player
import random
import bullets
import animob

class Monster( things.LivingThing ):
    NAME = "MONSTER"

    SPEED = 4
    DAMAGE = 1
    xdir = 1
    ydir = 1

    def update( self , levelmap ):
        if self.shield > 0:
            self.shield += -1

        self.do_ai( levelmap )

        if self.health < 1:
            self.die( levelmap )
            levelmap.contents.remove( self )

        else:
            for t in levelmap.contents:
                if isinstance( t , player.Player ) and self.is_touching( t ):
                    t.hurt( self.DAMAGE , self.liverect() , levelmap )

    def die( self , levelmap ):
        # This monster is dying. Maybe do something?
        pass

    def hit( self , levelmap ):
        # Default blood splatter.
        levelmap.contents.append( animob.BloodSplat( self.mid_x() - 16 , self.mid_y() - 16 ))

    def do_ai( self , levelmap ):
        # This is the monster's chance to act.
        self.update_patroller( levelmap )

    def update_patroller( self , levelmap ):
        # A patrolling monster just walks back and forth on its current platform.
        # It is affected by gravity.
        if levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            # If we haven't reached terminal velocity yet, apply acceleration.
            if self.dy < self.TERMINAL_VELOCITY:
                self.dy += 1
        elif self.delay > 0:
            self.delay += -1
            self.decelerate_x()
        else:
            # On solid ground. Just move back and forth.
            if self.dx == 0:
                self.xdir = random.randint( 0 , 1 ) * 2 - 1
                self.dx = self.xdir * self.SPEED

            if ( levelmap.is_an_obstacle(self.foot_x(), self.foot_y()-1) == False ) and levelmap.is_an_obstacle(self.foot_x()+self.dx, self.foot_y()-1):
                self.xdir = -self.xdir
            elif levelmap.is_a_space( self.foot_x() + self.dx , self.foot_y() ):
                self.xdir = -self.xdir
            self.dx = self.xdir * self.SPEED
        self.apply_dx( levelmap )
        self.apply_dy( levelmap )

    def update_wanderer( self , levelmap ):
        # A wandering monster just walks back and forth and doesn't care about falling
        # off of its platform. It is affected by gravity.
        if levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            # If we haven't reached terminal velocity yet, apply acceleration.
            if self.dy < self.TERMINAL_VELOCITY:
                self.dy += 1
        elif self.delay > 0:
            self.delay += -1
            self.decelerate_x()
        else:
            # On solid ground. Just move back and forth.
            if self.dx == 0:
                self.xdir = random.randint( 0 , 1 ) * 2 - 1
                self.dx = self.xdir * self.SPEED
            if ( levelmap.is_an_obstacle(self.foot_x(), self.foot_y()-1) == False ) and levelmap.is_an_obstacle(self.foot_x()+self.dx, self.foot_y()-1):
                self.xdir = -self.xdir
            self.dx = self.xdir * self.SPEED
        self.apply_dx( levelmap )
        self.apply_dy( levelmap )

    def update_faller( self , levelmap ):
        # This monster does nothing but sit there and be affected by gravity.
        if levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            # If we haven't reached terminal velocity yet, apply acceleration.
            if self.dy < self.TERMINAL_VELOCITY:
                self.dy += 1
        self.decelerate_x()
        self.apply_dx( levelmap )
        self.apply_dy( levelmap )

    def update_flier( self , levelmap ):
        if self.dx == 0:
            self.xdir = random.randint( 0 , 1 ) * 2 - 1
            self.dx = self.xdir * self.SPEED
        if self.dy == 0:
            self.ydir = random.randint( 0 , 1 ) * 2 - 1
            self.dy = self.ydir * self.SPEED

        if self.delay > 0:
            self.delay += -1
            self.decelerate_x()
        else:
            if ( levelmap.is_an_obstacle(self.mid_x(), self.mid_y()) == False ) and levelmap.is_an_obstacle(self.mid_x()+self.dx, self.mid_y()):
                self.xdir = -self.xdir
            self.dx = self.xdir * self.SPEED

        if ( levelmap.is_an_obstacle(self.mid_x(), self.mid_y()) == False ) and levelmap.is_an_obstacle(self.mid_x(), self.mid_y()+self.dy):
            self.ydir = -self.ydir
        self.dy = self.ydir * self.SPEED

        self.apply_dx( levelmap )
        self.y += self.dy

class AcidDragon( Monster ):
    NAME = "Acid Dragon"

    DAMAGE = 3
    SPEED = 2
    wander_now = True
    counter = 0
    recharge = 0

    def __init__( self , x , y ):
        super(AcidDragon, self).__init__(x,y,width=62,height=62,sprite_name="monster_dragon_acid.png",frame=0,topmargin=0,sidemargin=0,bottommargin=1,health=25)

    def do_ai( self , levelmap ):
        if self.wander_now:
            self.update_wanderer( levelmap )
        else:
            self.update_flier( levelmap )
        self.counter += -1
        if self.counter < 1:
            if random.randint( 1,3 ) == 2:
                self.wander_now = not self.wander_now
                self.ydir = -1
                self.counter = random.randint( 50 , 90 )
                if self.wander_now:
                    self.counter += 50
            elif not self.wander_now:
                self.wander_now = True
                self.counter = random.randint( 50 , 90 )
            else:
                self.dy = -8 - random.randint( 1 , 4 )
                self.counter = random.randint( 30 , 50 )
        self.recharge += 1
        if ( self.delay == 0 ) and ( self.recharge >= 240 ):
            self.breath_weapon( levelmap )
            self.recharge = 0

    def breath_weapon( self , levelmap ):
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , 5 , 0 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , -5 , 0 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , 0 , 5 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , 0 , -5 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , 3 , 3 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , 3 , -3 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , -3 , 3 , player.Player ))
        levelmap.contents.append( bullets.Acid( self.x + self.dx + 15 , self.y + self.dy + 15 , -3 , -3 , player.Player ))

    def die( self , levelmap ):
        # Do a big boom.
        levelmap.contents.append( animob.BigBoom( self.x + self.dx - 1 , self.y + self.dy - 1 , loop = 2 ))


class BlackBear( Monster ):
    NAME = "Black Bear"
    def __init__( self , x , y ):
        super(BlackBear, self).__init__(x,y,width=27,height=16,sprite_name="monster_blackbear.png",frame=0,topmargin=0,sidemargin=0,bottommargin=0,health=5)

class BlueSlime( Monster ):
    NAME = "Blue Slime"
    CAN_KNOCK_BACK = False
    DAMAGE = 3
    SPEED = 2
    wander_now = True
    counter = 0

    def __init__( self , x , y ):
        super(BlueSlime, self).__init__(x,y,width=32,height=32,sprite_name="monster_slime_blue.png",frame=0,topmargin=10,sidemargin=2,bottommargin=6,health=5)

    def do_ai( self , levelmap ):
        if self.wander_now:
            self.update_wanderer( levelmap )
        else:
            self.update_faller( levelmap )
        self.counter += -1
        if self.counter < 1:
            self.wander_now = not self.wander_now
            self.counter = random.randint( 10 , 20 )
            if random.randint( 1 , 4 ) == 1:
                self.xdir = 0

    def hit( self , levelmap ):
        levelmap.contents.append( animob.GreenSplat( self.mid_x() - 16 , self.mid_y() - 16 ))

class Bat( Monster ):
    NAME = "Bat"
    def __init__( self , x , y ):
        super(Bat, self).__init__(x,y,width=32,height=32,sprite_name="monster_bat.png",frame=0,topmargin=6,sidemargin=2,bottommargin=10,health=1)

    def do_ai( self , levelmap ):
        # This is the monster's chance to act.
        self.update_flier( levelmap )

class Frog( Monster ):
    NAME = "Giant Frog"
    counter = 0
    SPEED = 3

    def __init__( self , x , y ):
        super(Frog, self).__init__(x,y,width=32,height=32,sprite_name="monster_frog_green.png",frame=0,topmargin=4,sidemargin=2,bottommargin=5,health=5)

    def do_ai( self , levelmap ):
        self.update_patroller( levelmap )
        self.counter += 1
        if ( self.counter > 60 ) and not levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            self.dy = -8 - random.randint( 1 , 4 )
            self.counter = random.randint( 1 , 20 )

MANUAL = (Frog, Bat, BlueSlime, BlackBear, AcidDragon)


