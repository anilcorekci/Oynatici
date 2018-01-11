#! coding:utf-8 -*-
# vim: ts=8:sw=8

from widget  import sevilen
from gi.repository import GObject as gobject 
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
import os 
from config import conf
class tooltipview():
	def __init__(self,iconview,viewlist):
                self.view = viewlist
		self.liste = viewlist.sozluk
		self.data = None
		self.time = None
		self.x = None
		self.y = None
		self.iconView = iconview
		

		self.iconView.connect_object("motion-notify-event",self.monotify,self.iconView)
#		self.iconView.connect('leave-notify-event', self.on_leave )
		self.iconView.connect('button-press-event', self.on_leave )
		self.parent = self.iconView
		self.win = gobject.timeout_add(100,self.findparent)
        
		self.store = self.iconView.get_model()

		self.pop = sevilen.pop()
                
		self.pop.scale.connect("rating-changed",self.favor) 

	def findparent(self):
		self.parent = self.parent.get_parent()
		try:
			self.parent.connect('motion-notify-event', self.on_leave )	
			return True	
		except:
			gobject.source_remove(self.win)
			return False
	def favor(self,data,x):
		if self.data: 
			self.view.sevilen.set_conf(self.data,"rating",x) 
                        del self.view.sevilen
                        self.view.sevilen = conf.conf(self.view.svcfg)
	def on_leave(self,widget=None,event=None):
	        if widget and event:
                        if event.type ==  gdk.EventType.BUTTON_PRESS:
	        		self.pop.win.hide()
	        		self.data = True
                self.pop.win.hide()
	def tooltip(self,iv,event,pos):
		if self.data: 
                        return None 
                        
		x=   iv.get_root_window().get_pointer() [1]
		y = iv.get_root_window().get_pointer() [2]
		if self.x != x and self.y != y:
			return False		

                if  x >= self.width - self.width/4:
                        x -=  self.width/4
		self.pop.win.move( x+3, y+3)

                for filepath in self.view.sozluk:
                        self.data = filepath                                        
                        if self.title == self.view.get_value(filepath,"title") :
                                break
                        try:                                
                                if self.title == os.path.basename(filepath):                                     
                                        break
                        except AttributeError:
                                continue
                       # self.data = filter(lambda i:self.title == self.view.get_value(i,"title")  ,self.view.sozluk)[0]
    
                                
                genre = self.view.get_value(self.data,"genre")
                ar = self.view.get_value(self.data,"artist")
                al = self.view.get_value(self.data,"album")
                #image = self.view.get_value(self.data,"image")
                image = "Bilinmiyor"
                text = """<b>%s</b>\n<b>Tarz:</b> %s   
<b>Sanatçı:</b> %s  
<b>Album:</b> %s""" %(str(self.title),str(genre),str(ar),str(al)) 
 
                
                if image is "Bilinmiyor":
                        pix = self.view.dirIcon
      #          else:        
       #                 try:pix = self.view.geticon.get_pixbuf(image)
      #                  except:pix = self.view.dirIcon
                self.pop.image.set_from_pixbuf(pix)
                self.pop.label.set_markup(text.replace("&",""))

                if  self.data  in self.view.sevilen.sections():
                        
                        value = self.view.sevilen._get(self.data,"rating")
                        self.pop.scale.set_value(int(value) )
                else:                                                
                        self.pop.scale.set_value(0)
 
		self.pop.win.show_all()					
	def monotify(self, iv, event) :
		pos = iv.get_path_at_pos(int(event.x), int(event.y))                
                screen = event.get_screen() 
                self.width = screen.get_width()
		self.x=   iv.get_root_window().get_pointer() [1]
		self.y = iv.get_root_window().get_pointer() [2]

		if pos:
                        self.title =  self.store[pos] [0]
                        try:
                                gobject.source_remove(self.time)	
                        except TypeError:
                                del self.time                                
			self.time = gobject.timeout_add(1000,self.tooltip,iv,event,pos)
		else:
                        self.on_leave()
                        self.data = None	
