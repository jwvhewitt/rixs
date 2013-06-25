import things
import image
import bullets
import animob

class Player( things.LivingThing ):
    # Create some constants to tell the difference between different states.
    PCS_WALKING,PCS_FALLING = range( 2 )

    MAX_PC_SPEED = 6
    JUMP_SPEED = 10
    SLIDEYNESS = 2

    ATTACK_LENGTH = 6
    RECHARGE_LENGTH = 12

    ATTACK_TYPE = bullets.Sword

    def __init__(self, x=0, y=0 ):
        super(Player, self).__init__(x,y,width=32,height=32,sprite_name="default_player.png",frame=0,topmargin=4,sidemargin=8,bottommargin=1,health=10)
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.fire_button = False
        self.state = self.PCS_WALKING
        self.health_sprite = image.Image( "bitz_heart.png" , 22 , 22 )
        self.equip_sprite = image.Image( "bitz_equipment.png" , 32 , 32 )
        self.fire_dir = 1
        self.recharge = 0
        self.full_health = self.health
        self.potions = 0

        self.weapon = 0
        self.armor = 0


    def update( self, levelmap ):
        if self.shield > 0:
            self.shield += -1
        if self.recharge > 0:
            self.recharge += -1

        if self.fire_button and ( self.recharge == 0 ):
            levelmap.contents.append( self.ATTACK_TYPE( self.x + self.dx , self.y , self.fire_dir ) )
            self.recharge = self.RECHARGE_LENGTH
            if self.state != self.PCS_FALLING:
                self.delay = self.ATTACK_LENGTH

        if ( self.state == self.PCS_FALLING ) or levelmap.is_a_space( self.foot_x() , self.foot_y() ):
            # Free falling, just like Tom Petty.
            self.state = self.PCS_FALLING

            # If we haven't reached terminal velocity yet, apply acceleration.
            if self.dy < self.TERMINAL_VELOCITY:
                self.dy += 1

            # If the player is currently delayed, slow down horizontal speed just
            # to prevent them from flying off into space.
            if self.delay != 0:
                self.decelerate_x()

        elif self.delay > 0:
            self.delay += -1
            self.decelerate_x()

        else:
            if self.move_right:
                if self.dx < ( self.MAX_PC_SPEED * self.SLIDEYNESS ):
                    self.dx += 1
                    self.fire_dir = 1
                elif self.dx > ( self.MAX_PC_SPEED * self.SLIDEYNESS ):
                    self.dx += -1
            elif self.move_left:
                if -self.dx < ( self.MAX_PC_SPEED * self.SLIDEYNESS ):
                    self.dx += -1
                    self.fire_dir = -1
                elif -self.dx > ( self.MAX_PC_SPEED * self.SLIDEYNESS ):
                    self.dx += 1
            else:
                self.decelerate_x()

            if self.move_up:
                # There's a base JUMP_SPEED value, which gets modified by horizontal
                # speed. In other words, if you want to jump high, get a running start.
                self.dy = -self.JUMP_SPEED - abs( self.dx / ( self.SLIDEYNESS * 3 ) )
                self.state = self.PCS_FALLING

        # Handle motion now.
        # First, vertical movement- aka falling. This function will return True
        # if the player has just landed, so in that case set the state to walking.
        if self.apply_dy( levelmap ):
            self.state = self.PCS_WALKING


        truedx = self.dx / self.SLIDEYNESS
        # Check for moving into obstacles- if so, BOUNCE!
        if ( levelmap.is_an_obstacle(self.foot_x(), self.foot_y()-1) == False ) and levelmap.is_an_obstacle(self.foot_x()+truedx, self.foot_y()-1):
            self.dx = -self.dx
        elif ( levelmap.is_an_obstacle(self.head_x(), self.head_y()) == False ) and levelmap.is_an_obstacle(self.head_x()+truedx, self.head_y()):
            self.dx = -self.dx
        self.x += self.dx / self.SLIDEYNESS

    def hit( self , levelmap ):
        # Default blood splatter.
        levelmap.contents.append( animob.SmallBoom( self.mid_x() - 16 , self.mid_y() - 16 ))

    def render_health( self, screen ):
        # Draw the health bar for the PC.
        self.equip_sprite.render( screen , ( 15 , 450 ) , self.armor )
        self.equip_sprite.render( screen , ( 47 , 450 ) , self.weapon + 4 )
        for t in range( self.full_health ):
            if t < self.health:
                self.health_sprite.render( screen, ( t * self.health_sprite.frame_width + 79 , 450 ) , 0 )
            else:
                self.health_sprite.render( screen, ( t * self.health_sprite.frame_width + 79 , 450 ) , 1 )
        for t in range( self.potions ):
            self.health_sprite.render( screen, ( 602 - t * self.health_sprite.frame_width , 450 ) , 2 )

    def is_really_dead( self , levelmap ):
        # Check to see whether of not the PC is really dead
        if self.potions > 0:
            self.potions -= 1
            self.health = self.full_health
            levelmap.contents.append( animob.Twinkle( self.mid_x() - 16 , self.mid_y() - 16 ))
        return self.health < 1



