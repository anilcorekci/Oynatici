#! coding:utf-8 -*-
# vim: ts=8:sw=8
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import re
class findview():
	def __init__(self,iconview):
		self.iconView = iconview
		self.iconView.connect("key-press-event", self.key) 
		self.iconView.connect("button-press-event", self.keuv) 	
		self.pop = None
		self.show = None
		self.tr = None
		self.parent = iconview
		
		self.ret= [ "Return","Escape", "Control_R","Control_L"]
		self.utf8 = {'ccedilla':'ç',
				  'scedilla':'ş',
				  'gbreve':'ğ',
				  'period':'.',
				  'idotless':'ı',
				  'comma':',',
				  'udiaeresis':'ü',
				  'odiaeresis':'ö' 
				}
		self.win = gobject.timeout_add(100,self.findparent)	
	def findparent(self):
		self.parent = self.parent.get_parent()
		try:
			self.parent.connect('button-press-event', self.keuv )	
			return True	
		except:
			gobject.source_remove(self.win)
			return False
	def keuv(self,view,event):
		if self.show:
			self.pop.hide()
			self.en.set_text("")
			self.show = None
	def key (self,view,event):
		if not self.pop:
			builder = gtk.Builder()
			builder.add_from_file("./glade/ara.glade")
			self.pop = builder.get_object("window1")
			self.en = builder.get_object("entry1")
			self.en.connect("changed",self.enpress)
 
		else: 		
			keyname =  gdk.keyval_name(event.keyval)   
			if keyname in self.ret or \
			    len(keyname) > 1 and \
			    not keyname in self.utf8:return
                        root = view.get_window() 
			(x,tree_x, tree_y) =  view.get_window().get_origin()
			(tree_w, tree_h) =  root.get_width() ,root.get_height()
			x = tree_x + tree_w-180
			y = tree_y + tree_h
			if keyname in self.utf8:
				self.tr = self.utf8[keyname]  
			self.pop.move(x  ,y  ) 
			self.pop.show_all()
	#		if len(keyname) == 1 or keyname in self.utf8:  
#				self.en.emit("key-press-event",event)
#				self.enpress(self.en,event)
			self.show = True	
	def enpress(self,w,event=None ):
  
		text = w.get_text() 
		if  len(text) <= 0: return
		self.exper = re.compile(text)
		lis = []  
		self.iconView.select_all()
		model = self.iconView.get_model()
		item = self.iconView.get_selected_items()

		for x in item: 
			iter = model.get_iter(x)
			lis.append(model[iter][0])
			ln = filter(self.exper.search,lis)
			if len(ln) >= 1: 
				self.iconView.unselect_all()
				self.iconView.select_path(x)
				try:
				        self.iconView.scroll_to_path(x[0], True, 0.8,0.5)
				except TypeError:
				        pass
				return
		self.iconView.unselect_all()		

