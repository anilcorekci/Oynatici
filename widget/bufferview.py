#! coding:utf-8 -*-
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
import os
from widget import createbutton
class buffer():
    def __init__(self,view,last_dir):
        self.buffer = {"undo":[],"undo_start":None,
					   "redo":[],"redo_start":None} 
        self.current_directory = last_dir
        self.last = last_dir
        view.connect("dir-changed",self.data)
        self.view = view
        self.up = createbutton.rlb(   gtk.STOCK_GO_UP ,"Yukarı",1,self.upp) 
        self.und = createbutton.rlb(   gtk.STOCK_GO_BACK ,"Geri Al",1,self.undo) 
        self.red = createbutton.rlb(gtk.STOCK_GO_FORWARD,"Tekrar Yap",1,self.redo)
    def data(self,w,directory):
        self.current_directory = directory
        if not self.current_directory in self.buffer["redo"]:	
            self.buffer["redo"] = [] 
            self.buffer["redo_start"] = None
            self.red.set_sensitive(False)

        if not self.buffer["undo"]:
            self.buffer["undo_start"] = self.current_directory
        self.up.set_sensitive(True)	
        self.buffer["undo"].append(self.current_directory)			
        sensitive = True	
        if self.current_directory == self.last:sensitive =False
        self.und.set_sensitive(sensitive)
    def upp(self,data=None):
        if not self.buffer["redo_start"]:
            self.buffer["redo_start"] = self.current_directory
        self.buffer["redo"].append(self.current_directory)
        self.current_directory = os.path.dirname(self.current_directory)
        if self.current_directory == "/":
            self.up.set_sensitive(False)		
        self.view.current_directory =  self.current_directory
        self.view.fill_store()	
    def undo(self, data=None):
        if not self.buffer["redo_start"]:
            self.buffer["redo_start"] = self.current_directory
        self.buffer["redo"].append(self.current_directory)

        index = self.buffer["undo"].index(self.current_directory)    
        index = self.buffer["undo"][index -1 ] 
        self.current_directory  = index
	
        sensitive = True
        if self.current_directory == self.buffer["undo_start"]:
            sensitive = False
            self.buffer["undo"] = []
            self.buffer["undo_start"] = None
        self.und.set_sensitive(sensitive)
	
        self.buffer["redo"].append(self.current_directory)

        self.red.set_sensitive(True)
        self.view.current_directory =  self.current_directory
        self.view.fill_store()	
    def redo(self,data=None):
        index = self.buffer["redo"].index(self.current_directory)	
        index = self.buffer["redo"][index -1 ] 
	 
        sensitive = True 
        if index == self.buffer["redo_start"] :
            sensitive = False
            self.buffer["redo"] = []
            self.buffer["redo_start"] = None
	 
        self.current_directory  = index	
        self.red.set_sensitive(sensitive)	
        self.und.set_sensitive(True)
        self.view.current_directory =  self.current_directory
        self.view.fill_store()	
 


