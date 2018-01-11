# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
def rlb( stock, tooltext,size,kontak=None ):
	image = gtk.Image()
	try:
		pix = gdkpixbuf.Pixbuf.new_from_file_at_size(stock,18,18)
		image.set_from_pixbuf(pix)
	except Exception:          
		image.set_from_stock( stock ,size)  
	item = gtk.Button() 
	item.set_relief(gtk.ReliefStyle.NONE)
	item.set_tooltip_text(tooltext)
	if kontak:
		item.connect('clicked',kontak)
	item.add(image)
	# item.set_flags(gtk.CAN_DEFAULT)
	item.set_focus_on_click(False) 
	item.show_all()
	return item                     
def toggle(stock,text,label=None):
    tog = gtk.ToggleButton()
    image =gtk.Image() 
    if stock in gtk.stock_list_ids():
        image.set_from_stock( stock ,1)  
    else:
        try:
            pix = gdkpixbuf.Pixbuf.new_from_file_at_size(stock,20,20)
            image.set_from_pixbuf(pix)
        except Exception:     
            image.set_from_icon_name(stock,1)
    hbox = gtk.HBox()
    if label :
        info = gtk.Label(label)
        hbox.pack_end(info,True,True,2)
    hbox.pack_start(image,True,True,2)        
    tog.add(hbox) 
    tog.set_relief(gtk.ReliefStyle.NONE) 
    tog.set_tooltip_text(text)         
    # tog.set_flags(gtk.CAN_DEFAULT)
    tog.set_focus_on_click(False) 
    return tog	
 
 
