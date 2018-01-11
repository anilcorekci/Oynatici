#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
class menu():
    def __init__(self,widget,button= 3,tooltip=None ):
        self.tooltip = tooltip
        self.button = button
        self.widget = widget  
        self.menu = gtk.Menu()
        self.widget.connect_object("button-press-event",self.button_press,  self.menu)
            
    def add_item(self,stock,kontak,arg=None,check=None): 
        if check:
            Item  = gtk.CheckMenuItem(stock)
        else:
            Item  = gtk.ImageMenuItem(stock)
        if arg is None:
            Item.connect('activate',  kontak  )      
        else:
            Item.connect('activate',  kontak,arg  )                                              
        self.menu.append(Item)
        self.menu.show_all()			
        return Item
    def button_press(self, widget, event):
        if self.tooltip : self.tooltip.on_leave()
        if event.button == self.button:
            widget.popup(None, None,None, None, event.button, event.time)
            return True
        else:
            return False
