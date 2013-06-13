import things
import monster

class Bullet( things.Thing ):
    DAMAGE = 1
    LIFESPAN = 999

    def __init__(self, x=0, y=0, width=64, height=64, sprite_name="", frame=0, topmargin=0, sidemargin=0, bottommargin=0, dx=0, dy=0, target=things.LivingThing ):
        super(Bullet, self).__init__(x,y,width,height,sprite_name,frame,topmargin,sidemargin,bottommargin)
        self.count = 0
        self.target = target
        self.dx = dx
        self.dy = dy

    def update( self, levelmap ):
        self.x += self.dx
        self.y += self.dy
        self.count += 1

        if levelmap.is_an_obstacle( self.x + self.width / 2 , self.y + self.height / 2 ) or self.count >= self.LIFESPAN:
            levelmap.contents.remove( self )
        else:
            for t in levelmap.contents:
                if isinstance( t , self.target ) and self.is_touching( t ):
                    t.hurt( self.DAMAGE , self.liverect() , levelmap )
                    self.count = self.LIFESPAN


class Sword( Bullet ):
    LIFESPAN = 5
    SPEED = 8
    DAMAGE = 2

    def __init__(self, x=0, y=0, dx=0, dy=0, target=monster.Monster ):
        super(Sword, self).__init__(x,y,width=32,height=32,sprite_name="bullet_sword.png",topmargin=8,sidemargin=4,bottommargin=8,target=target)
        if dx > 0:
            self.frame = 1
        self.dx = dx * self.SPEED
        self.x += self.dx
        self.dy = dy
        self.y += self.dy

class Acid( Bullet ):
    LIFESPAN = 50

    def __init__(self, x=0, y=0, dx=0, dy=0, target=monster.Monster ):
        super(Acid, self).__init__(x,y,width=32,height=32,sprite_name="bullet_acid.png",topmargin=0,sidemargin=0,bottommargin=0,target=target)
        self.dx = dx
        self.x += self.dx
        self.dy = dy
        self.y += self.dy

