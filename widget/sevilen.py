#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf as gdkpixbuf
from gi.repository import GObject as gobject
from widget import geticon

 
class sevilen(  gtk.EventBox):
    def __init__(self , size=17 ):
        gtk.EventBox.__init__(self) 
        self.size =  size
        self.cursor = None
        
        self.add_events(gdk.EventMask.ALL_EVENTS_MASK)


        
        self.box = gtk.HBox()
        
        self.sev_image_list = []

        for x in range(0,5):     self.sev_image_list.append( gtk.Image()  )
        
        for x in self.sev_image_list: self.box.pack_start(x,False,False,self.size/4)
        
        
        self.add(self.box)
        
        self.geticon = geticon.get_icon()
        
        self.active_pix = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/star.svg",self.size,self.size)
        self.deactive_pix = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/star_grey.svg",self.size,self.size)
        
        self.clear()
        
        self.connect("button-press-event",self.tikla)
        self.connect("motion-notify-event",self.notify)
        
        self.kac_ = 0
        self.sev_ = 0
 
 
    def clear(self):
        for w in self.sev_image_list : w.set_from_pixbuf(self.deactive_pix)
    def set_value(self,numara):
        self.clear()
        for i in range(0,numara): 
            self.sev_image_list[i].set_from_pixbuf( self.active_pix)                
        self.sev_ = numara            
    def set_(self,numara):
        self.kac_ = numara               
        self.clear()
        for i in range(0,numara): 
            self.sev_image_list[i].set_from_pixbuf( self.active_pix)                

    def notify(self,widget,event):
        if self.cursor is None:
            self.draw = self.get_window()
            self.sec =   gdk.Cursor( gdk.CursorType.HAND1)
            self.draw.set_cursor(self.sec)
            self.cursor = True
            
        if event.x > self.size  : self.set_(1)
        if event.x > self.size*2 : self.set_(2)
        if event.x > self.size*3 + self.size/3 : self.set_(3)    
        if event.x > self.size*4 + self.size/2 : self.set_(4)    
        if event.x > self.size*5 + self.size   : self.set_(5)    
        if event.x < self.size/2 or   event.x > self.size*6+ self.size or \
            event.y < self.size/2 or event.y > self.size *2:  self.set_(self.sev_)    
 
    def tikla(self,widget,event) :  
        if event.button: 
            self.sev_ =  self.kac_
            self.emit("rating-changed",self.sev_)
            
class pop(gtk.Builder):
    def __init__(self):
        gtk.Builder.__init__(self)
        self.add_from_file("./glade/pop.glade") 
        self.win = self.get_object("window1")
        self.vbox = self.get_object("vbox1")
        self.label = self.get_object("label1")
        self.scale = sevilen()
        self.vbox.pack_end(self.scale,False,False,10)
        self.image = self.get_object("image1")
        self.label.modify_fg(gtk.StateType.NORMAL,  gdk.color_parse("#D5D5D5"))   
        self.win.modify_bg(gtk.StateType.NORMAL,  gdk.color_parse("#000000"))   
        self.scale.modify_bg(gtk.StateType.NORMAL,  gdk.color_parse("#000000"))   

gobject.signal_new("rating-changed", sevilen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_INT,))
