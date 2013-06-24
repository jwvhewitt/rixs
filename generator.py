import things
import animob

class Generator( things.Thing ):
    # A Generator creates new things- usually monsters, maybe bullets, whatever.

    def __init__(self, x=0, y=0, product=None, number=1, frequency=150 ):
        super(Generator, self).__init__(x,y,width=32,height=32,sprite_name="special_sprites.png",invisible=True)
        self.product = product
        self.children = []
        self.counter = 0
        self.number = number
        self.frequency = frequency

    def update( self , levelmap ):
        self.counter += 1
        if self.counter > self.frequency:
            self.counter = 0
            if len( self.children ) < self.number:
                # Create a new child.
                c = self.product( x = self.x , y = self.y )
                self.children.append( c )
                levelmap.contents.append( c )

                c = animob.BlueBoom( x = self.x , y = self.y , loop = 2 )
                levelmap.contents.append( c )
            else:
                # Check to see if any children need to be removed.
                for c in self.children:
                    if c not in levelmap.contents:
                        self.children.remove( c )


