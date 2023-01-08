"""A bounding box for the balls so they don't escape
    all over the screen
"""
class Bounds():

    """Construct the box

    Parameters
    ----------
    x : int
        X position on the display
    y : int
        Y position on the display
    w : int
        Width of bounds
    h : int
        Height of bounds
    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    """Draw the bounding box

    Parameters
    ----------
    fg : colour
        The border colour
    bg : colour
        The background colour
    display : PicoGraphics
        The display to draw on
    """
    def draw(self, fg, bg, display):
        display.set_pen(bg)
        display.clear()
        display.set_pen(fg)
        display.rectangle(self.x - 1, self.y - 1, self.w + 2, self.h + 2)
        display.set_pen(bg)
        display.rectangle(self.x, self.y, self.w, self.h)
            
"""Ball class"""
class Ball():
    """Construct a new ball

    Parameters
    ----------
    p : Vector
        The position vector
    v : Vector
        The velocity vector
    r : int
        Radius of ball
    c : colour
        Colour of ball
    """
    def __init__(self, p, v, r, c):
        if not isinstance(p, Vector) or not isinstance(v, Vector):
            return NotImplemented
        
        self.v = v
        self.p = p
        self.r = r
        self.c = c
        self.m = self.v.magnitude()

    """Draw the ball on the display

    Parameters
    ----------
    display : PicoGraphics
        The display to draw on
    bounds : Bounds
        The bounding box
    """
    def draw(self, display, bounds):
        display.set_pen(self.c)
        display.circle(int(self.p.x + bounds.x), int(self.p.y + bounds.y), self.r)

    """Move the ball and bounce off the bounding box

    Parameters
    ----------
    bounds : Bounds
        The bounding box
    """
    def move(self, bounds):
        
        # Move the position
        # self.p += self.v * (self.v.magnitude() * 4)
        
        # Optimised by storing magnitude (our balls don't change speed)
        self.p += self.v * (self.m * 4)
        
        # Bounce off the walls and move inside if gone out of bounds
        if self.p.x - self.r < 0:
            self.p.x = self.r
            self.v.x *= -1            

        if self.p.x + self.r > bounds.w:
            self.p.x = bounds.w - self.r
            self.v.x *= -1
            
        if self.p.y - self.r < 0:
            self.p.y = self.r
            self.v.y *= -1
            
        if self.p.y + self.r > bounds.h:
            self.p.y = bounds.h - self.r
            self.v.y *= -1
    
"""Sort of works :)
        if COLLISION_DETECTION:
            for targetBall in balls:
                if not (
                    ball.p.y + ball.r < targetBall.p.y - targetBall.r or
                    ball.p.y - ball.r > targetBall.p.y + targetBall.r or
                    ball.p.x + ball.r < targetBall.p.x - targetBall.r or
                    ball.p.x - ball.r > targetBall.p.x + targetBall.r
                ):
                    # collided
                    originalV = ball.v
                    ball.v = targetBall.v
                    targetBall.v = originalV
"""                    
    
"""Vector class code borrowed from github, could be any vector class"""
class Vector():
    def __init__(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            return NotImplemented
        self.x = x
        self.y = y
    def __add__(self, addingVector):
        if not isinstance(addingVector, Vector):
            return NotImplemented
        return Vector(self.x+addingVector.x, self.y+addingVector.y)
    def __sub__(self, subingVector):
        if not isinstance(subingVector, Vector):
            return NotImplemented
        return Vector(self.x-subingVector.x, self.y-subingVector.y)
    def __mul__(self, multiplier):
        if not isinstance(multiplier, (int, float)):
            return NotImplemented
        return Vector(self.x * multiplier, self.y * multiplier)
    def __rmul__(self, multiplier):
        return self.__mul__(multiplier)
    def __truediv__(self, divisor):
        if not isinstance(divisor, (int, float)):
            return NotImplemented
        return Vector(self.x / divisor, self.y / divisor)
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
    def normalise(self):
        divisor = self.magnitude()
        if divisor != 0:
            self.x /= divisor
            self.y /= divisor
        else:
            raise ZeroDivisionError
    @property
    def unit_vector(self):
        if not isinstance(vector, Vector):
            return NotImplemented
        divisor = self.magnitude()
        if divisor != 0:
            return self / divisor
    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)