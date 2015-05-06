'''
Created on 11 Apr 2015

@author: Benjamin
'''
import kivy

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse

class DraggableWidget(Widget):

    def __init__(self, colour, boundaries, **kwargs):
        '''
        Initialises an instance of the DraggableWidget class.
        
        Input parameters:
            colour: a 3 element list (with values between 0 to 1) representing red, green 
                and blue, respectively. This will be the colour of the circle.
            boundaries: a 4 element list containing the left, right, bottom and top 
                boundary coordinates, respectively. This restricts where the widget can
                be dropped.
        '''
        super(DraggableWidget, self).__init__(**kwargs)
        
        self.bounds = boundaries   
        
        # Stores the position of the widget before it is dragged.        
        self.reset_position()   
        
        # Represents where the user has touched the widget relative to the origin.
        self.offset_x = 0
        self.offset_y = 0
                    
        self.being_dragged = False         
        
        
        # Draws the graphical representation of the widget - an ellipse.
        with self.canvas:
            Color(colour[0], colour[1], colour[2])
            self.graphic = Ellipse(pos = (self.x, self.y), size = self.size)
        
    def on_touch_down(self, touch):
        '''
        Handles the initial touch event for the widget.
        '''
        
        # If the user's touch is within the bounds of the DraggableWidget, we set a variable so 
        #     we know we are currently being dragged, and we store the original position so
        #     we can undo the drag if necessary.
        if self.collide_point(touch.x, touch.y):
            self.being_dragged = True
            self.reset_position()
            
            # Stores the position of the touch relative to the widget's origin
            #     so that the widget can stay at this offset position while 
            #     being dragged.
            self.offset_x = touch.x - self.x
            self.offset_y = touch.y - self.y
        
    def on_touch_up(self, touch):
        '''
        Handles the touch event for the widget when the screen is released, checking for
            collisions with other widgets and whether it is out of bounds.
        '''
        
        self.being_dragged = False
        
        # We check whether the widget is positioned within the valid boundaries and store
        #     the resulting boolean value.
        out_of_bounds = self.x < self.bounds[0] or (self.x + self.width) > self.bounds[1] \
            or self.y < self.bounds[2] or (self.y + self.height) > self.bounds[3];
        
        # Searches for other DraggableWidget objects and puts them in a list
        circles = []
        for circle in self.parent.children:
            if isinstance(circle, DraggableWidget):                
                if (circle.id != self.id):
                    circles.append(circle)     
            
        # Boolean value that is only set to False when there is more than one collision
        #     with another DraggableWidget object
        valid_collision = True;
        
        # Stores a DraggableWidget being collided with.
        colliding_widget = None;
        
        # Check through the other DraggableWidget objects to find collisions
        for circle in circles:
            if self.collide_widget(circle):
                if colliding_widget == None:
                    colliding_widget = circle;
                else:
                    valid_collision = False
                    break                
        
        # If the widget is out of bounds or has collided with another DraggableWidget, we
        #     reset its position. If not, we allow it to stay where has been dragged,
        #     and we store a new original position.
        if (out_of_bounds or colliding_widget != None):
            self.x = self.original_x
            self.y = self.original_y
            self.graphic.pos = (self.x, self.y)
        else:
            self.reset_position()
            
        # If we have collided with a single other DraggableWidget object, we display a message
        if (valid_collision and colliding_widget != None):        
            self.parent.collide_text(self, colliding_widget)   
            
        if (out_of_bounds):
            self.parent.out_of_bounds_text(self)
        
    def on_touch_move(self, touch):
        '''
        Handles the touch event 
        '''
        if self.being_dragged:
            self.x = touch.x - self.offset_x
            self.y = touch.y - self.offset_y
            self.graphic.pos = (self.x, self.y)
    
    def reset_position(self):
        self.original_x = self.x
        self.original_y = self.y