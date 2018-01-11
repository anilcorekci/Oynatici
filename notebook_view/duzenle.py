# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gtk as  gtk
from gi.repository import Gdk as  gdk
import os
import re
from set_tag import mutagen_meta 
class duzenle():
    def __init__(self,viewlist):

        self.viewlist = viewlist
        self.iconView = self.viewlist.iconView1
        
        builder = gtk.Builder()
        builder.add_from_file("./glade/düzenle.glade")

        self.pen = builder.get_object("window1")
        self.pen.connect("delete-event",self.close)
        self.note =  builder.get_object("notebook1")
        self.file = builder.get_object("entry1")
        self.file.modify_base(gtk.StateType.NORMAL,  gdk.color_parse("#D0BC92"))   
        self.artist = builder.get_object("entry2")
        self.album = builder.get_object("entry3")
        self.genre = builder.get_object("entry4")
        self.song = builder.get_object("entry5")
        self.label = builder.get_object("label1")
        
        self.once = builder.get_object("button1")
        self.sonra = builder.get_object("button2")
        
        self.once.connect("clicked",self.git_once)
        self.sonra.connect("clicked",self.git_sonra)
        
        self.tag_list =  {"artist":self.artist,"album":self.album,"genre":self.genre,"title":self.song}
        
    def close(self,w,data):
        self.save_metadata()
        self.pen.hide()
        return True  
    def save_metadata(self):
        file_ = self.file.get_text()
        for x in  self.tag_list:
            entry_text = self.tag_list[x].get_text()
            mutagen_meta.set_tag(file_,x,entry_text )           
            self.viewlist.pick.change(self.viewlist.pick.ek(file_),x,entry_text)   
    def git_once(self,data):
        self.save_metadata()
        if self.bul():
            self.goster("blablablal")
    def git_sonra(self,data):
        self.save_metadata()
        if self.bul(True):
            self.goster("blabla")

    def bul(self,neyi=False):    
        liste = filter(lambda i:self.ar == self.viewlist.get_value(i,"artist") \
                            and self.al == self.viewlist.get_value(i,"album") ,\
                            self.viewlist.sozluk)
        title_list = [ self.viewlist.get_value(i,"title")   for i in liste]                       

  
        if neyi is False:
            self.path -=1 
            onceki = title_list[self.path ] 
            self.sec(onceki)
            return onceki
        if neyi is True:
            try:
                sonraki  = title_list[self.path + 1]            
            except IndexError:
                return False
            self.path +=1                    
            self.sec(sonraki)
            return sonraki            
    def sec(self,text):
        self.iconView.select_all()
        model = self.iconView.get_model()
        item = self.iconView.get_selected_items()

            
        for x in  item :
            iter = model.get_iter(x )

            if model[iter][0] ==  text:
                self.iconView.unselect_all()           
                self.iconView.select_path(x )
                break                    				
    def goster(self,xxx=None):
        model = self.iconView.get_model()
        item = self.iconView.get_selected_items() 
        self.name = None            

        for x in enumerate(item):
            iter = model.get_iter(x[1])
            self.path = x[0]
            self.name = model[iter][0] 
                   
        print self.path            
        if self.name is None: return            
        file_ = filter(lambda i:self.name == self.viewlist.get_value(i,"title") \
                            or self.name == os.path.basename(i),self.viewlist.sozluk)[0]
        genre = self.viewlist.get_value(file_,"genre")
        self.ar = self.viewlist.get_value(file_,"artist")
        self.al = self.viewlist.get_value(file_,"album")                
 
                     
        self.song.set_text(self.name) ; self.artist.set_text(self.ar)
        self.genre.set_text(genre) ; self.album.set_text(self.al)
        self.label.set_text("%s  - %s" %(self.ar,self.name) )
        self.file.set_text(file_)        
        if True is self. viewlist.get_value(file_,"video"):
            self.note.set_sensitive(False)    
        else:
            self.note.set_sensitive(True)                               
        if xxx is None:  self.pen.show_all()
