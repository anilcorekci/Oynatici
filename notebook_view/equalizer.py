#! coding:utf-8 -*-
# vim: ts=8:sw=8
from gi.repository import Gtk as gtk
from gi.repository import Gst as gst
from config import conf
import os

cachedir = os.environ["HOME"].strip("\n")+"/"+".oynatıcı/"
eq =   cachedir+"equalizer.cfg"
vd =  cachedir+"videobalance.cfg"

class equalizer(gtk.VBox): 
	def __init__(self,player,hide):
		gtk.VBox.__init__(self)
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./glade/equalizer.glade")      
		note = self.builder.get_object("notebook1")
		self.pack_start(note,True,True,1)
					
		self.eqconf =  conf.conf(eq)
		self.vdconf =  conf.conf(vd)
		self.player = player
		self.player_mode()
		
		self.builder.get_object("button1").connect("clicked",self.set_data,"sıfırla") 
		self.builder.get_object("button2").connect("clicked",lambda data:self.set_data("ozel") )
		self.builder.get_object("button3").connect("clicked",self.set_data,"kaydet")			
		
                self.builder.get_object("button8").connect("clicked",lambda data:hide() )	
                
		self.set_data("vdozel") 
		self.set_data("ozel") 
	 
                 
	def player_mode(self):	
 #	equalizer ! audioconvert ! autoaudiosink ...
		self.eq   = gst.ElementFactory.make('equalizer-10bands')
		audioconvert = gst.ElementFactory.make('audioconvert')
		audiosink = gst.ElementFactory.make('autoaudiosink')
		sinkbin = gst.Bin()
		for element in (self.eq, audioconvert, audiosink):
		        sinkbin.add(element)
		self.eq.link(audioconvert)
                audioconvert.link(audiosink)
                sinkpad = self.eq.get_static_pad('sink')	
                pad = gst.GhostPad.new('sink', sinkpad)
                sinkbin.add_pad( pad	)
		self.player.set_property('audio-sink', sinkbin)
		

	def set_data(self,data=None,band=None):	
		if data == "ozel":
			liste = self.eqconf.sections() ; liste.sort()
			for i,x in zip(range(10),liste):
				band = "band%s"  %(i)
				vscale = self.builder.get_object(band)
				vscale.connect("value-changed",self.set_data,band)
				val = self.eqconf._get(x,"value")
				vscale.set_value(float(val) )	
		elif band:
			if band == "sıfırla": 
				for i in range(10):
					band = "band%s"  %(i)
					self.builder.get_object(band).set_value(0.0)
			elif band == "kaydet":
				for i in  range(10) : 
					band = "band%s"  %(i)
					vscale = self.builder.get_object(band)
					self.eqconf.set_conf(band,"value",str(vscale.get_value() ) )
					self.eqconf.yaz()		
			else: self.eq.set_property(band,data.get_value() )
