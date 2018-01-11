#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import Gdk as gdk
import os,thread
from gi.repository import Gst as gst

class progress():
    def __init__(self,icv,tag,viewlist):
        self.icv = icv 
        self.view_list = viewlist
        self.tag = tag
        self.sozluk = tag.pik.sozluk
        
        self.pipeline = gst.ElementFactory.make("playbin", "None")  
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.sink = gst.ElementFactory.make("fakesink") 
        self.pipeline.set_property("audio-sink", self.sink)
        self.pipeline.set_property("video-sink", self.sink)            

        
        self.build = gtk.Builder()
        self.build.add_from_file("./glade/progress.glade")
        self.pen = self.build.get_object("window1")
        self.expander = self.build.get_object("expander1")
        self.nexpander = self.build.get_object("expander2")
        self.pen.connect("delete-event",self.hide)
        self.pro  = self.build.get_object("progressbar1")
        self.buffer = self.build.get_object("textbuffer1")
        self.nbuffer = self.build.get_object("textbuffer2")
        self.label = self.build.get_object("label1")
        self.nlabel = self.build.get_object("label2")
        
        self.uri = ""
        self.ress = None
        self.control = {}
    def fake(self,uri):
        self.uri = uri

        if self.ress:
            self.pipeline.set_state(gst.State.NULL)
            self.pipeline.set_property("uri", "file://"+uri)
            self.pipeline.set_state(gst.State.PLAYING)
        else:
            self.ress = True
    def on_message(self, bus, message):
        t = message.type  
 
        if t == gst.MessageType.TAG:       
            tags=message.parse_tag()                          
            self.tag.system(tags,self.uri,True) 
            self.i +=1
            self.eklenen.append(self.uri)
            self.pipeline.set_state(gst.State.NULL)   
        elif t == gst.MessageType.ERROR:
            self.i +=1          
            err, debug = message.parse_error()            
            self.eklenemiyen[self.uri] = "%s" %(err)
            self.pipeline.set_state(gst.State.NULL)           
        elif t == gst.MessageType.EOS:
            self.i +=1            
            self.eklenemiyen[self.uri] = "Bilgi bulunamadı.."  
            self.pipeline.set_state(gst.State.NULL)           
    def ekle(self):
        self.pen.show_all()
        thread.start_new_thread(self.ther, ())  
    def ther(self):           
        gdk.threads_enter()	  
        self.pro.set_text("Dizinler Okunuyor...")        
        gdk.threads_leave()	         
        model = self.icv.iconView.get_model()
        item = self.icv.iconView.get_selected_items()
        self.ls = []
        for x in item:
            y=self.icv.current_directory+ "/"+model[x][0] 

            if not y in self.ls:        
                if os.path.isdir(y):     self.dizin(y)
                else:  self.ls.append(y)     	        

        self.hide()      
        self.eklenemiyen = {}
        self.eklenen = []          
        self.i = 0             
        try:
            x = 1.0/ len(self.ls) 
        except ZeroDivisionError:
            self.bitir()
            return False
        i = 0.0
        self.ress = True
        self.fake (self.ls[self.i] )
        
        gdk.threads_leave()	  
        while True:   	
            if self.ress is None:
                self.bitir()
                break  
            try:                
                if self.pipeline.get_state(True)[1] == gst.State.NULL:
                    text = self.ls[self.i]   
                    if text in self.sozluk:
                        self.eklenen.append(text )   
                        i += x        
                        self.i+=1 
                        continue 

                    self.fake (text)
                    i += x
            except IndexError:
                self.bitir()
                break                      
            else:  
                if i != self.pro.get_fraction():
                    gdk.threads_enter()	  
                    self.pro.set_fraction(i)
                    self.pro.set_text("Belgeliğe Ekleniyor.. %s öğede (%s) " %(len(self.ls),self.i+1)  )
                    gdk.threads_leave()	  
                    
    def dizin(self,filename):
        for x in os.listdir(filename):
            if filename+"/"+x in self.ls:
                return True
            if  os.path.isdir( filename+"/"+x):
                self.dizin(filename+"/"+x)
            else:        
                self.ls.append( filename+"/"+x)    
                               
    def bitir(self):
        self.ress = None
        self.pro.set_text("Belgeliğe Eklendi. (%s) " %(self.i) )
        self.pro.set_fraction(1.0)        
        
        self.label.set_text("Eklenen Dosyalar.. ( %s) " %(len(self.eklenen)  ) )
        self.nlabel.set_text("Eklenemeyen Dosyalar.. ( %s) " %(len(self.eklenemiyen) ) )
        
        self.buffer.insert_at_cursor("\n\n".join(self.eklenen) ) 
        x = [ "%s\n(%s)\n"%(x,self.eklenemiyen[x]) for x  in self.eklenemiyen] 
        self.nbuffer.insert_at_cursor("\n".join(x) ) 
        
        self.expander.set_sensitive(True)          
        self.nexpander.set_sensitive(True)   
 
    def hide(self,w=None,data=None):
    
        self.label.set_text("Eklenen Dosyalar.." )
        self.nlabel.set_text("Eklenemeyen Dosyalar.." )
        self.expander.set_expanded(False)
        self.expander.set_sensitive(False)       
        self.nexpander.set_expanded(False)
        self.nexpander.set_sensitive(False)           
        self.nbuffer.set_text("")
        self.buffer.set_text("")
        self.pro.set_text("Belgeliğe Ekleniyor...")
        self.pro.set_fraction(0.0)
        
        if w and data:
            self.pen.hide() 
            self.view_list.check_list(self.view_list.sozluk)
            self.ress = None
            return True
 
