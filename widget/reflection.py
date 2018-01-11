#!/usr/bin/python
# -*- coding: utf-8 -*-

# ZetCode PyGTK tutorial 
#
# This program creates an
# image reflection
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2011


import  gtk
import cairo,gst
class reflection():
    def __init__(self,area,icon,player):
        self.area = area
        self.player = player
 
        self.area.connect("expose-event", self.expose)
 
        
        try:
            self.surface = cairo.ImageSurface.create_from_png(icon)
        except Exception, e:
            print e.message
 
        
        
        self.imageWidth = self.surface.get_width()
        self.imageHeight = self.surface.get_height()
        self.gap = 50
 

 
    
    def expose(self, widget, event):
        if self.player.get_state()[1] !=  gst.STATE_PAUSED and \
                self.player.get_state()[1] !=  gst.STATE_PLAYING:
                        cr = widget.window.cairo_create()

                                   
                        w = self.area.get_parent().allocation.width
                        h =  self.area.get_parent().allocation.height
 
                        cr.paint()
                        
                        cr.set_source_surface(self.surface, w/2-w/4, h/12)
                        cr.paint()

                        alpha = 0.5
                        step = 1.0 / self.imageHeight
                      
                        cr.translate(0, 2 * self.imageHeight + self.gap)
                        cr.scale(1, -1)
                        
                        i = 0
                        
                       
                        while(i < self.imageHeight+w):

                            cr.rectangle(w/2-w/4, self.imageHeight-i , self.imageWidth, 1)

                            i = i + 1
                            
                            cr.save()
                            cr.clip()
                            cr.set_source_surface(self.surface,w/2-w/4, h/12)
                            alpha = alpha - step
                            cr.paint_with_alpha(alpha)
                            cr.restore()
        

 
