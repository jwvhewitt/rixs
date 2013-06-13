import things

class AnimOb( things.Thing ):
    def __init__(self, x=0, y=0, width=64, height=64, sprite_name="", start_frame=0, end_frame=0, ticks_per_frame = 1, loop = 0 ):
        super(AnimOb, self).__init__(x,y,width,height,sprite_name,start_frame)
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.ticks_per_frame = ticks_per_frame
        self.counter = 0
        self.loop = loop

    def update( self, levelmap ):
        self.counter += 1
        if self.counter > self.ticks_per_frame:
            self.frame += 1
            self.counter = 0

        if self.frame <= self.end_frame:
            self.x += self.dx
            self.y += self.dy
        else:
            self.loop += -1
            if self.loop < 0:
                levelmap.contents.remove( self )
            else:
                self.frame = self.start_frame
                self.counter = 0

class BigBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(BigBoom, self).__init__(x,y,64,64,"fx_bigboom.png",0,9,2,loop)

class BloodSplat( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(BloodSplat, self).__init__(x,y,32,32,"fx_damage.png",12,14,1,loop)

class BlueBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(BlueBoom, self).__init__(x,y,32,32,"fx_damage.png",6,8,1,loop)

class EarthBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(EarthBoom, self).__init__(x,y,32,32,"fx_damage.png",18,20,1,loop)

class GreenBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(GreenBoom, self).__init__(x,y,32,32,"fx_damage.png",9,11,1,loop)

class GreenSplat( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(GreenSplat, self).__init__(x,y,32,32,"fx_damage.png",21,23,1,loop)

class PinkBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(PinkBoom, self).__init__(x,y,32,32,"fx_damage.png",27,29,1,loop)

class RedBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(RedBoom, self).__init__(x,y,32,32,"fx_damage.png",0,2,1,loop)

class SmallBoom( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(SmallBoom, self).__init__(x,y,32,32,"fx_damage.png",3,5,1,loop)

class Sonic( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(Sonic, self).__init__(x,y,32,32,"fx_damage.png",24,26,1,loop)

class Zap( AnimOb ):
    def __init__(self, x=0, y=0, loop=0 ):
        super(Zap, self).__init__(x,y,32,32,"fx_damage.png",12,14,1,loop)


