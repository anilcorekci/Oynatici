#!/usr/bin/env python
#! coding:utf-8 -*-
# vim: ts=4:sw=4
import sys,os,gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk 


dizin = os.environ["HOME"].strip("\n")+"/"+".oynatıcı"
if not os.path.isdir(dizin):
        os.makedirs(dizin)
cp = ["./config/mms.cfg","./config/equalizer.cfg","./config/videobalance.cfg"]  
for x in cp: 
	fil = "%s%s" %(dizin, x.replace("./config","") )
	if not os.path.isfile(fil):
		os.system('cp  %s "%s" ' %(x,dizin) )    
from gui import player
oynatici = player() 
if len(sys.argv) >= 2: 
	for x in sys.argv[1:]:
		name = os.path.basename(x)
		oynatici.liste[name] = x
		oynatici.treestore.append(None, [name])  
 
if __name__  == "__main__":
	gdk.threads_init() 
	gtk.main()				
