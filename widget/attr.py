#! coding:utf-8 -*-
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
class stil():   
    def __init__(self,label,gobject):
        self.info = label 
        self.info.set_alignment(0,-1)                 
      #  self.info.set_selectable(True)
        
        self.i =  0.99        
 

        self.fx = gobject.timeout_add(250,self.kayan)

    def kayan(self) :      
        self.i-=0.01
        if self.i <= 0.00:
            self.i= 0.99 
        else:         
            self.info.set_alignment(self.i,-1)                            
        return True
