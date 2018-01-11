# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
class volgui(gtk.HBox):
    def __init__(self,player):
        gtk.HBox.__init__(self)
        self.player = player
        self.exval = 0.50  
        self.volsize = 1
        self.button = gtk.ToggleButton()
        self.button.connect("toggled",self.click)
        self.button.set_relief(gtk.ReliefStyle.NONE) 
        
        self.image = gtk.Image()
        self.image.set_from_icon_name("audio-volume-medium",self.volsize)
        
        self.button.add(self.image)       
     #    self.button.set_flags(gtk.CAN_DEFAULT)
        self.button.set_focus_on_click(False)
        
        self.adj = gtk.Adjustment() 
     #    self.adj.set_all(-1, 0.0,1 , 0.1)   
        self.adj.set_upper(1)
        self.scale = gtk.HScale() #self.adj) 
        self.scale.set_adjustment(self.adj)
        self.adj.connect("value_changed" , self.change)
        self.scale.connect("motion-notify-event",self.convert_vol)
        self.scale.connect("button-press-event",self.convert_vol)
        self.scale.set_draw_value(False)
        self.scale.set_can_focus(False)
        self.scale.set_size_request(100,-1)
        self.scale.set_value(self.exval)
        
        self.pack_start(self.button,False,False, 1)
        self.pack_end(self.scale,False,False, 1)

    def val_string(self,value=None):
        if  value is None:
            value = self.scale.get_value()
        if value == 1.0: val = "100"
        else:val =  str(value)[2:4]
        if len(val) <= 1:  val = val+"0" 
        val = val +" %"     
        return val
    def convert_vol(self,w,event):
        mouse_x, mouse_y = event.get_coords()
        scale_loc = w.get_allocation() 
        value = mouse_x / scale_loc.width     
        if event.type == gdk.EventType.MOTION_NOTIFY:
            val = self.val_string(value)
            w.set_tooltip_text(val)
        if event.type == gdk.EventType.BUTTON_PRESS:
            self.scale.set_value(value)
    def click(self,data):
        if data.get_active():
            self.exval = self.scale.get_value()
            self.scale.set_value(0)
        else:
            self.scale.set_value(self.exval)                   
    def change(self, data):
        val = data.get_value()
        val = float(str(val)[:4]) 
        self.player.set_property('volume', val)         
        if val  == 0.0:
            self.image.set_from_icon_name("audio-volume-muted",self.volsize)
        else:
            if self.button.get_active():
                self.button.set_active(False)            
        if val  >  0:
            self.image.set_from_icon_name("audio-volume-low",self.volsize) 
        if val  >  0.5:
            self.image.set_from_icon_name("audio-volume-medium",self.volsize)                          
        if val  == 1.0:
            self.image.set_from_icon_name("audio-volume-high",self.volsize)              
        self.button.set_tooltip_text(self.val_string())                           
