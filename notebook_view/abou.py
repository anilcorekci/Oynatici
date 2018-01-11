#! coding:utf-8 -*-
# vim: ts=4:sw=4
from gi.repository import GObject as gobject
from gi.repository import GdkPixbuf as gdkpixbuf
from gi.repository import Gtk as gtk
class hakkinda():
    def __init__(self):        
        self.i = 0.6
        self.hak = gtk.AboutDialog()	
        self.hak.set_title("Oynatıcı `. ) ")
        self.hak.set_decorated(False)
        self.hak.set_program_name("Oynatıcı `. )")
        self.hak.set_version("0.1.0") 
        self.hak.set_copyright("UGT..")
        self.hak.set_icon_from_file("./simgeler/oynatıcı.png")
        self.hak.connect("delete-event", lambda w, data: self.hak.destroy())
        self.hak.set_license("GPL")
        mail=["hitokiri  <anilcorekci@gmail.com>"]
        self.hak.set_authors(mail)
        logo = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/oynatıcı.png", 148, 148)
        self.hak.set_logo(logo)	
        self.id = gobject.timeout_add(500,self.opacity)
        self.hak.show_all()
 #       if  self.hak.run() == gtk.ResponseType.CANCEL:             
        if  self.hak.run() < 0:             
            gobject.source_remove(self.id)
            self.hak.destroy()
    def opacity(self): 
        #:P XD `. )
        if  self.i >= 0.9: self.i = 0.6
        self.i +=0.1
        self.hak.set_opacity(self.i)    
        return True
        
