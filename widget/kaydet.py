# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
import os
from gi.repository import Gtk as gtk
from time import gmtime, strftime
from widget import createmenu

class kaydet(gtk.Button):
    def __init__(self,play):
        gtk.Button.__init__(self)
        self.play = play
        self.set_relief(gtk.ReliefStyle.NONE)

        image = gtk.Image()
        image.set_from_stock( gtk.STOCK_INDEX ,1)
        self.add(image)
       # self.connect("clicked",self.kaydet_fark)
        self.menu = createmenu.menu(self ,1)
        self.menu.add_item( gtk.STOCK_OPEN, self.kaydet )
        self.menu.add_item( gtk.STOCK_SAVE, self.save )   
        self.menu.add_item( gtk.STOCK_SAVE_AS, self.kaydet_fark  )
    def dialog(self,action,stock,text=""):
        dialog = gtk.FileChooserDialog(text,
                                       				 None,
                                       				 action,
                                      				 (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
                                       				 stock, gtk.ResponseType.OK))	
        dialog.set_default_response(gtk.ResponseType.OK)
     #    dialog.set_current_name(u"Çalma Dizelgesi.pls")
        pls = gtk.FileFilter()
        pls.set_name("pls")
        pls.add_pattern("*pls")
        dialog.add_filter(pls)
        return dialog
    def save(self,data): 
        liste = [self.play.liste[x] for x in self.play.liste]
        view = self.play.view_list
        saat_tarih = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        view.dizelge.sozluk[saat_tarih] = liste
        view.dizelge.yaz()
        view.check_list(view.sozluk)        
    def kaydet (self,data):
        dialog  = self.dialog(gtk.FileChooserAction.OPEN,gtk.STOCK_OK,"Çalma Dizelgesini Aç")
        if dialog.run() == gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.play.ekpls(filename)
        dialog.destroy()            
    def kaydet_fark(self,data):
        liste = [self.play.liste[x] for x in self.play.liste]
        dialog = self.dialog(gtk.FileChooserAction.SAVE ,gtk.STOCK_SAVE,"Çalma Dizelgesini Kaydet")
        response = dialog.run()   	
        if response ==  gtk.ResponseType.OK:
            bilgi = dialog.get_filename()
            with open(bilgi,"w") as dosya:
                info = "[playlist]\nNumberOfEntries=%s\n" %(len(liste)+1  )
                dosya.write(info)
                [dosya.write("file%s=%s\n"%(y+1,x) ) for x ,y in zip(liste,range(len(liste))) ]        
            dosya.close()		            
        dialog.destroy()                                                 
 
