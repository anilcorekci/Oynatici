#! coding:utf-8 -*-
# vim: ts=4:sw=4
import   os,time,re,random
from gi.repository import GObject as gobject
from gi.repository import GdkPixbuf as gdkpixbuf

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkX11
import gi
gi.require_version('GstVideo', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gst as gst
gst.init(None)
from gi.repository import GdkX11, GstVideo

import   urllib 
import cairo
from gui import tag  
from widget import (
    createbutton,
    kaydet,
    sevilen,
   # attr,
    volgui)
from notebook_view import(
    mms,
    arsiv,
    equalizer,
    view_list,
    abou)    
pix_data = """/* XPM */
 static char * invisible_xpm[] = {
 "1 1 1 1",
 "       c None",
 " "};"""
TARGET_TYPE_URI_LIST = 80
dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]
home = os.environ["HOME"].strip("\n")
 

class player(object):  
    def __init__(self):    
        self.playing = None 
        self.istasyon = None
        self.play_thread_id= None
        self.dur_time = None
        self.eq = None
        self.liste = {}
        self.pixbuf ='./simgeler/rhythmbox-missing-artwork.svg'               
        self.pos  = 0
        self.shuffle = None
        self.ress = None 
        self.relo = False
        self.time =  "00:00 / 00:00"
       #     self.manager =  gtk.recent_manager_get_default()
    
        self.window = gtk.Window()  
        self.window.resize(720,560) 
        self.window.connect("delete_event",self.closex)  
        self.window.set_title("Oynatıcı .` ) ") 
        self.window.set_icon_from_file("simgeler/oynatıcı.png")
        
        self.movie_window = gtk.DrawingArea() 
     #       self.movie_window.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
     #     gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
     #     dnd_list, gtk.gdk.ACTION_COPY)    
        self.movie_window.connect('drag_data_received', self.on_drag_data_received)
        self.movie_window.add_events(gdk.EventMask.ALL_EVENTS_MASK)
        self.movie_window.set_size_request(150,150)
        self.movie_window.connect_object("button-press-event", self.press,
                                  self.menu([ gtk.STOCK_MEDIA_PLAY,
                                      gtk.STOCK_MEDIA_FORWARD, 
                                      gtk.STOCK_MEDIA_REWIND,
                                      gtk.STOCK_MEDIA_NEXT,
                                      gtk.STOCK_MEDIA_PREVIOUS, 
                                      "Ses Dengesi"     ,  
                                     #   "Ekran Görüntüsü Al",    
                                      gtk.STOCK_ABOUT ] )   )
        self.movie_window.modify_bg(gtk.StateType.NORMAL,  gdk.color_parse("#000000"))   
        self.movie_window.connect_object("scroll-event", self.scroll,True) 
        self.movie_window.connect_object("motion-notify-event",self.monotify,self.movie_window)

        self.player = gst.ElementFactory.make("playbin", "None")     
        
 #
     #   reflection.reflection(self.movie_window,"./simgeler/oynatıcı.png",self.player)
 
        visplug = gst.ElementFactory.make("goom",None)#libvisual_infinite
        self.player.set_property('vis-plugin', visplug)
        self.player.set_property("flags",15)
 
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
 
        self.adj = gtk.Adjustment()
        self.spinner = gtk.HScale()
        self.spinner.set_adjustment(self.adj)
      #       self.spinner = gtk.ProgressBar(self.adj)
        self.spinner. set_draw_value(False)
        self.spinner.add_events(gdk.EventMask.ALL_EVENTS_MASK)
        self.spinner.connect("motion-notify-event",self.convert_time )
        self.spinner.connect("button-press-event",self.convert_time )
   #       self.spinner.connect_object("scroll-event", self.scroll,True) 
        self.adj.connect("value_changed" , self.change)

        
        self.hx = gtk.HBox()        
        self.image = gtk.Image()
        self.image.set_from_stock(gtk.STOCK_MEDIA_PLAY,3)

        buton = gtk.Button()
        buton.set_relief(gtk.ReliefStyle.NONE)
        buton.connect("clicked",self.play)
        buton.add(self.image)  
        buton.set_focus_on_click(False)
        
        onceki = createbutton.rlb(  gtk.STOCK_MEDIA_PREVIOUS ,"Önceki",3,self.onceki )         
        sonraki = createbutton.rlb(  gtk.STOCK_MEDIA_NEXT ,"Sonraki",3,self.sonraki )         
        cus = createbutton.rlb(  gtk.STOCK_MEDIA_STOP ,"Durdur",1,self.stop)         
        

 
   
        box = gtk.HBox() 
        shuffle = createbutton.toggle( "media-playlist-shuffle" ,"Rastgele Oynat")     
        shuffle.connect("toggled", self.shuf  )      
        
        repeat = createbutton.toggle(  "media-playlist-repeat" ,"Tekrar Kipi")     
        repeat.connect("toggled",self.reload)      
        
        box.pack_start( shuffle,False,False,1 )
        box.pack_start( repeat,False,False,1 ) 
        box.pack_start( cus,False,False,1 )

        box.pack_start( onceki,False,False,1  )
        box.pack_start( buton,False,False,1 )
        box.pack_start( sonraki,False,False,1 )       
 
    #    self.spinner.set_size_request(200,-1)
   #     self.spinner.set_can_focus(False)
#        box.pack_start(self.spinner,True,True,1 )   

        vol = volgui.volgui(self.player) 
        box.pack_start(  vol,False,False,1 )   
                
        self.favo =   sevilen.sevilen() 
        self.favo.get_style_context().add_class(gtk.STYLE_CLASS_MENUBAR)
        
        
        bix = gtk.VBox() 
        self.info = gtk.Label() ,gtk.Label() , gtk.Label() 
        for x in self.info: 
            x.set_alignment( 0.99,-1)    
            x.set_selectable(True)     
            x.set_size_request(200,-1)
            bix.pack_start(x,False,False,0 )

        box.pack_end(bix,True,True,6 )           
        box.pack_start(   self.favo,False,False,10 )   
  
        self.hx.pack_start(box,True,True,1 ) 
        

        self.infobox = gtk.EventBox()
        self.infobox.get_style_context().add_class(gtk.STYLE_CLASS_MENUBAR)  
        self.infobox.add_events(gdk.EventMask.ALL_EVENTS_MASK)
        self.infobox.connect("scroll-event",self.scr)
        bt = gtk.HBox()  
        
    #  #  self.info.set_alignment( 0,-1)          
        bt.pack_start(self.hx,True,True,3 ) 
       #   self.hx.pack_end( box,False,False)
        self.infobox.add(bt)
 
 

 

        self.viewarea = gtk.VBox()


        vbox = gtk.VBox()
 
        self.pro = gtk.ProgressBar()
        self.sta = gtk.Label()  
        box = gtk.HBox()     
        self.cubuk = createbutton.toggle(  gtk.STOCK_GOTO_LAST,"Kenar Çubuğu ")  
        self.cubuk.connect("toggled",self.tik)
        mini = createbutton.toggle( "zoom-out" ,"Başa Dön")     
        mini.connect("toggled", self.mini  )           

        self.spinner.set_size_request(200,-1)
        self.spinner.set_can_focus(False)
        

        box.pack_start(self.spinner,True,True,4 )    
        box.pack_end( self.cubuk,False,False,2)        
        box.pack_end( mini,False,False,2)    
        box.pack_end( self.pro,False,False,2)            
        box.pack_end(self.sta,False,False,4 )    
        box.set_border_width(5)
        
        self.panel = box
        
        
        vx = gtk.VBox()
        
    #     vx.pack_start(self.info, False,False,0)
        vx.pack_end(self.infobox ,False,False,6)
        vbox.pack_start(self.ev_style(vx) ,False,False,0)
        
        vbox.pack_end(self.ev_style(box), False, False,0)


        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.PositionType.BOTTOM) 
        self.notebook.set_can_focus(False)
        self.notebook.set_scrollable(True)    
 
        paned = gtk.VPaned()     
        self.ble = gtk.HBox()
        self.ble.set_border_width(4)
        self.equi =equalizer.equalizer(self.player,self.eko)
        self.ble.pack_start(self.equi,True,True,3) 

        paned.pack1(self.movie_window, resize=False, shrink=False)    
        paned.pack2(self.ble, resize=False, shrink=False)
        self.append_tab("Şu An Yürütülen","./simgeler/oynatıcı.png",paned)
 
        self.tag = tag.tag(self.player,self.info)
 
        self.view_list = view_list.hbox(self,self.tag.pik) 
        self.append_tab("Belgelik","./simgeler/rhythmbox-missing-artwork.svg",self.view_list)          
        self.append_tab("Dosya Tarayıcı","./simgeler/folder_.png",self.viewarea)   
               
 
        widget = mms.filesel()
        widget.station = self.station
        self.append_tab("Genel Ağ Yayınları","./simgeler/mms.png",widget)          
 

        self.ply = self.notebook.render_icon(gtk.STOCK_MEDIA_PLAY,1,None)
        self.paus =  self.notebook.render_icon(gtk.STOCK_MEDIA_PAUSE,1,None)      
        
    
        self.area = gtk.Image()
        self.area.add_events(gdk.EventMask.ALL_EVENTS_MASK)

        self.area.connect("event",self.iko)
        self.area.connect("button-press-event",self.press)
        bax = gtk.VBox(False,False)

        bax.pack_start(self.ev_style(self.area ) ,False,False,0)
        hpaned = gtk.HPaned()
 
        hpaned.pack2(bax, False,  False)
        vbox.pack_start(hpaned ,True,True,0)    

        self.treestore = gtk.TreeStore(str)
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.connect("row-activated",lambda w,x,y:self.oynat() )
        self.treeview.set_headers_clickable(True)


        self.treeview.set_rules_hint(True)
     #   self.treeview.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
    #     gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
    #     dnd_list, gtk.gdk.ACTION_COPY)    
        self.treeview.connect('drag_data_received', self.on_drag_data_received)
 
        self.tvcolumn = [None]
        cellpb = gtk.CellRendererPixbuf()
        self.tvcolumn[0] = gtk.TreeViewColumn("\t",  cellpb) 
        self.tvcolumn[0].set_cell_data_func(cellpb, self.file_pixbuf)
        self.treeview.append_column(self.tvcolumn[0])
        cell = gtk.CellRendererText()
        self.tvcolumn[0] = gtk.TreeViewColumn(" Çalma Dizelgesi",  cell ) 
        self.tvcolumn[0].set_cell_data_func(cell, self.file_name)
     #   cell.set_property("scale",pango.SCALE_SMALL)
        self.treeview.append_column(self.tvcolumn[0])
        self.treeview.set_headers_visible(False)
 

        
        kal = createbutton.rlb( gtk.STOCK_STOP ,"Kaldır ",1,self.kal)  
 
        yukari =  createbutton.rlb( gtk.STOCK_GO_UP ,"Yukarı Taşı",1,self.up) 
        alt = createbutton.rlb( gtk.STOCK_GO_DOWN ,"Aşağı Taşı",1,self.down) 



        self.sw = gtk.ScrolledWindow()
        self.sw.add(self.treeview)
        self.sw.set_policy(True,True)
        ba = gtk.HBox(True,True)

        
 
        kaydt = kaydet.kaydet(self)
        ba.pack_start(kaydt ,False,False,10)         
        ba.pack_end(kal ,False,False,10)         
        ba.pack_end(alt,False,False,10) 
        ba.pack_end(yukari,False,False,10) 

        bax.pack_end( self.ev_style(ba ) ,False,False,0)
        bax.pack_start(self.sw,True,True,0)
        self.bax = bax



        hpaned.pack1( self.notebook  , False, False)

 
        self.window.add(vbox)  
        self.window.show_all()
        
        self.window.resize(850,600)
        

      #    self.attr = attr.stil(self.info,gobject) 
     #   
        dialog = arsiv.filesel(self,self.tag,self.view_list) 
 
        self.iconview = dialog
        self.viewarea.add(self.iconview) 
        self.iconview.show_all()       
   #     self.iconview.find.set_active(False)
   #     self.iconview.box.hide()
        
 
        self.widget = self.hx,self.ble,self.sta,self.infobox,self.panel,bax 
        self.pro.hide()
        self.ble.hide()
        self.cubuk.set_active(True)
        self.iko(self.area,True)     

    #      color = gtk.gdk.Color()
   #       self.draw = self.movie_window.get_window()
   #       pix = gtk.gdk.pixmap_create_from_data(self.draw , pix_data, 1, 1, 1, color, color) 
    #      self.invisible = gtk.gdk.Cursor(pix, pix, color, color, 0, 0) 
  #        self.normal =  gtk.gdk.Cursor(gtk.gdk.LEFT_PTR) 
    def scr(self,w,event):
        print (event.direction , gdk.EventScroll().direction.UP)
        if event.direction ==  gdk.EventScroll().direction.SMOOTH:
            self.notebook.next_page()
        if  event.direction ==  gdk.EventScroll().direction.DOWN:
            self.notebook.next_page()  
    def ev_style(self,widget,style=gtk.STYLE_CLASS_MENUBAR):
        ev = gtk.EventBox()
        ev.add(widget)
        ev.get_style_context().add_class(gtk.STYLE_CLASS_MENUBAR)  
        return ev
 
    def append_tab(self,text,pix_file,widget):
        box = gtk.HBox()
        label = gtk.Label(text) 
        label.set_alignment(0.1,0.5) 
        image = gtk.Image()
        pix = gdkpixbuf.Pixbuf.new_from_file_at_size(pix_file,20,20)
        image.set_from_pixbuf(pix)
        box.pack_start(image,False,False,1) 
        box.pack_end(label,False,False,1)      
        image.set_can_focus(False)    
        label.set_can_focus(False)    
        box.set_can_focus(False)            
        box.show_all()     
        self.notebook.insert_page( widget,box,-1)                
    def mini(self,data):
        if data.get_active(): 
           self.notebook.hide();self.cubuk.set_active(False)         
           self.window.resize(100,100)
        else: self.notebook.show() 
    def tik(self,data):
        if data.get_active(): 
            self.bax.show() 
            self.notebook.set_show_tabs(True)
            self.notebook.set_show_border(True)
        else:             
            self.notebook.set_show_tabs(False)
            self.notebook.set_show_border(False)
            self.bax.hide()          
    def eko(self ): 
        if self.eq is None:self.eq = True; self.ble.show()  
        else: self.eq = None;self.ble.hide()  

    def convert_time(self,w,event ):    
        bol = None
        if  self.adj.get_value() <= 1:return 
        if event.type == gdk.EventType.BUTTON_PRESS:
           if event.button == 3 or event.button ==1:
               bol = True
        elif event.type ==  gdk.EventType.MOTION_NOTIFY:pass        
        else:return    
        mouse_x, mouse_y = event.get_coords()
        scale_loc = w.get_allocation() 
        value = mouse_x / scale_loc.width 
        try:
           length =  self.player.query_duration(gst.Format.TIME)[1]
        except:return    
        seconds = float(value * length  )
        if bol:self.adj.set_value(seconds)
        else:w.set_tooltip_text( self.convert_ns(seconds) +" / "  
                         + self.convert_ns(length)   )
    def  reload(self,data=None):
        print data.get_active()
        self.relo  =data.get_active()      
    def shuf(self,data=None):
        self.shuffle = data.get_active()        
    def press(self,widget,event):        

 
 
        if event.button == 3: 
            widget.popup(None, None, None , None ,event.button, event.time)  
        elif event.type == gdk.EventType._2BUTTON_PRESS :
            self.window.fullscreen()  
             #     self.draw.set_cursor(self.invisible)   
            [x.hide() for x in self.widget]
            self.notebook.set_show_tabs(False)
            self.notebook.set_show_border(False)
        elif event.button == 1:           
            self.window.unfullscreen()
            [x.show() for x in filter(lambda i:i != self.ble and i !=self.bax,self.widget)]       
      #         self.draw.set_cursor(self.normal)   
            self.notebook.set_show_tabs(True)
            self.notebook.set_show_border(True)

    def file_pixbuf(self, column, cell, model, iter,xx):
        name = model.get_value(iter, 0) 
        xname = unicode(name,"utf-8")
        try:path = self.playing
        except AttributeError:
           cell.set_property('pixbuf', None) 
           return
        try:
           xpath =  self.liste[ name]           
        except KeyError:
           xpath = self.liste[xname]
        except Exception:
           return                                
        if path == xpath :
           if self.image.get_stock()[0] != "gtk-media-pause":
               cell.set_property('pixbuf', self.ply)
           else:cell.set_property('pixbuf', self.paus)
           try:
            self.pos = model.get_path(iter) [0]
           except:
            pass 
        else: cell.set_property('pixbuf', None) 
        return
    def file_name(self, column, cell, model, iter,xx):
        cell.set_property('text', model.get_value(iter, 0))
        return
 
           
    def iko(self,widget, event): 
 
        if event == True:
           widget.reset_rc_styles()
           style = self.window.get_style().copy()
           widget.set_style(style)
 
        w = widget.get_allocated_width()
        h =  widget.get_allocated_height()
 
        widget.set_size_request(w/2-w/12,210 )
        try:
            pix=  gdkpixbuf.Pixbuf.new_from_file_at_size(self.pixbuf,w/2-w/12+40*2,200)
        except:
            pix = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/rhythmbox-missing-artwork.svg",w/2-w/12+40*2,200)
        self.area.set_from_pixbuf(pix)      
        
    def get_file_path_from_dnd_dropped_uri(self,uri):
        path = ""
        if uri.startswith('file://'): 
           path = uri[7:] 
        path = urllib.url2pathname(path)
        path = path.strip('\r\n\x00') 
        return path
    def on_drag_data_received(self,widget, context, x, y, selection, target_type, timestamp):

        if target_type == TARGET_TYPE_URI_LIST:
           uri = selection.data.strip('\r\n\x00')
           uri_splitted = uri.split() 
           treeselection = self.treeview.get_selection()
           for uri in uri_splitted:
               filename = self.get_file_path_from_dnd_dropped_uri(uri)
               name = os.path.basename(filename)
               if name in self.liste:return
               self.liste[name] = filename
               self.treestore.append(None, [name])        
               treeselection.set_mode(gtk.SelectionMode.MULTIPLE)
               self.treeview.set_rubber_banding(True)

           
    def monotify(self, iv, event) : 
        
        screen = event.get_screen() 
        yscr = 50.0 
        wx,wy = self.window.get_size() 
        if wy == screen.get_height():
            if  event.y >= yscr:
                self.hx.hide() ;self.infobox.hide(),self.panel.hide()
            elif  event.y <= yscr:
                self.hx.show() ;self.infobox.show() 
            if event.y >= wy -100:
                self.panel.show()
               
    def hkn(self,data): 
        if data == True:
           self.movie_window.show() ;self.viewarea.hide()
        else:
           self.movie_window.hide() ;self.viewarea.show()
 
    def down(self,data=None):
        treeselection = self.treeview.get_selection()
        (model, rows) =  treeselection.get_selected_rows()
        for x in rows:
           iter = model.get_iter(x)
           pos = model.get_path(iter)      
           try:riter = model.get_iter(  (int(pos[0] ) +1)  )    
           except ValueError: pass
           else:model.swap(  iter ,riter) 
    def up(self,data=None):
        treeselection = self.treeview.get_selection()
        (model, rows) =  treeselection.get_selected_rows()
        for x in rows:
           iter = model.get_iter(x)
           pos = model.get_path(iter)   
           if int(pos[0]) > 0:  
               riter = model.get_iter(  (int(pos[0] ) -1)  )
               model.swap( iter ,riter)
 
    def oynat(self):  
        if self.image.get_stock()[0] == "gtk-media-stop":
           self.image.set_from_stock(gtk.STOCK_MEDIA_PLAY,3)
           self.stop()
           return
        treeselection = self.treeview.get_selection()
        (model, rows) =  treeselection.get_selected_rows()
        
 
        for x in rows:
           iter = model.get_iter(x)
           select =   model.get_value(iter, 0) 
           xselect = unicode(select,"utf-8")
           try:
               path = self.liste[select] 
           except KeyError:
               path = self.liste[xselect]
        try:
           self.start_stop(path)
        except UnboundLocalError: 
            self.image.set_from_stock(gtk.STOCK_MEDIA_PLAY,3)
     #      self.info.set_text("")
            self.pixbuf = './simgeler/rhythmbox-missing-artwork.svg'       
            self.iko(self.area,True)
    def onceki(self,data):
        treeselection = self.treeview.get_selection() 
        
        try:
           if int(self.pos) < 1: pass
        except:return
        else:       
           treeselection.unselect_all()
           self.pos -=1
           if self.pos  < 0:
                self.pos = 0
           treeselection.select_path(self.pos)  
           self.image.set_from_stock(gtk.STOCK_MEDIA_PAUSE,3)        
           self.oynat()
    def sonraki(self,data):
        treeselection = self.treeview.get_selection()     
        treeselection.unselect_all()     

        if self.relo:self.pos -=1  
        self.pos +=1 
        try: 
           treeselection.select_path(self.pos)         
        except : 
           return
        if self.shuffle:
           select = random.randint(0, len(self.liste) ) 
           treeselection.unselect_all()     

           try:
               treeselection.select_path(select)         
           except:
                treeselection.select_path(self.pos-1)         
           self.pos = select
        self.image.set_from_stock(gtk.STOCK_MEDIA_PAUSE,3)    
        self.oynat()
        if self.relo: 
            self.player.set_state(gst.State.PLAYING)
            self.image.set_from_stock(gtk.STOCK_MEDIA_PAUSE,3)       
    def kal(self,data=None):
        treeselection = self.treeview.get_selection()
        (model, rows) = treeselection.get_selected_rows()
        for x in rows:
           try:iter = model.get_iter(x)
           except ValueError:self.kal(True);return
           name = model[iter][0]
           try: del self.liste[name]    
           except KeyError:pass
           model.remove(iter)  
           self.pos -=1  
           if name in self.playing:
               self.stop()
               self.sonraki(True)
    def ek(self,data=None,view1=None):
        
        treeselection = self.treeview.get_selection() 
        treeselection.set_mode(gtk.SelectionMode.MULTIPLE)
        self.treeview.set_rubber_banding(True)
 
        if  not self.playing and self.pos <= 0:
            treeselection.select_path(0) 
            self.oynat()       
           
 
    def dizin(self,filename):
        for x in filter(lambda i:i not in self.liste,os.listdir(filename) ):
           if  os.path.isdir( filename+"/"+x):
               self.dizin(filename+"/"+x)
           else:    
               self.liste[x] = filename+"/"+x
               self.treestore.append(None, [x])        


    def play(self,data):     self.oynat() 
    
    def change(self,data):
 
        if data.get_value() != self.pos_int:
           self.player.seek_simple(gst.Format.TIME, gst.SeekFlags.FLUSH, data.get_value()  )      
 
    def play_thread(self) :    
        self.sta.set_text(  "00:00 / 00:00") 
        
        if self.dur is None:
            dur_int =  self.player.query_duration(gst.Format.TIME)[1]
            print (dur_int)
            if dur_int == -1:
                return True
            self.dur = dur_int 
              #  self.adj.set_page_increment( dur_int  )
            self.adj.set_upper(dur_int)
            return True
            
        dur_str = self.convert_ns(self.dur) 
        self.sta.set_text( "00:00 / " + dur_str) 

  #      self.adj.set_lower(0)
        pos_str = "00:00"
        try:
            self.pos_int =  self.player.query_position(gst.Format.TIME)[1]
            self.adj.set_value(self.pos_int) 
        except: return True
        try:            
            pos_str = self.convert_ns(self.pos_int)         
        except: return True
 
        self.time =   pos_str + " / " + dur_str
        self.sta.set_text(  pos_str + " / " + dur_str) 
        return True


    def scroll(self,w,event):
        if  event.direction == gdk.EventScroll().direction.UP:
           self.durak(True)
        elif event.direction ==  gdk.EventScroll().direction.DOWN:
           self.durak(False)      
    def durak(self,val):
        if val:
            pos_int =self.player.query_position(gst.Format.TIME)[1]
            print (pos_int)
            seek_ns = pos_int + (10 * 1000000000) 
            self.player.seek_simple(gst.Format.TIME, gst.SeekFlags.FLUSH, seek_ns) 
        elif not val:
            pos_int =self.player.query_position(gst.Format.TIME)[1]
            seek_ns = pos_int - (10 * 1000000000)
            self.player.seek_simple(gst.Format.TIME, gst.SeekFlags.FLUSH, seek_ns)                      
    def menu(self,item):     
        menu = gtk.Menu()
        for x in item: 
           menu_items = gtk.ImageMenuItem(x)
           menu.append(menu_items)
           menu_items.connect("activate", self.menuitem_response, x)
           menu_items.show()
        return menu
    def menuitem_response(self, widget, string): 
        if string == "gtk-media-play":
           if self.image.get_stock()[0] == "gtk-media-pause":
               self.player.set_state(gst.State.PAUSED)
               self.image.set_from_stock(gtk.STOCK_MEDIA_PLAY, 3)
           else:
               self.player.set_state(gst.State.PLAYING)
               self.image.set_from_stock(gtk.STOCK_MEDIA_PAUSE,3)
        elif string == "gtk-media-forward":self.durak(True)      
        elif string == "gtk-media-rewind": self.durak(False)      
        elif string == "gtk-media-next": self.sonraki(True)
        elif string == "gtk-media-previous": self.onceki(True)
        elif string == "Ses Dengesi":self.eko()                      
        elif string ==  "Ekran Görüntüsü Al":    
           al = self.movie_window.get_allocation()
           width = al.width
           height = al.height
           screenshot = gdkpixbuf.Pixbuf.get_pixels(
                    gdkpixbuf.Pixbuf( gdk.RGBA, True, 8, width, height),
                    self.movie_window.get_window(),
                    gdk.colormap_get_system(),
                    0, 0, 0, 0, width, height) 
           screenshot.save("%s/%s.%s." %( home,self.window.get_title().replace("/",".") , 
                      self.time.replace("/","-") ) + "png", "png" )
           del screenshot
        elif string == "gtk-about":abou.hakkinda()

    def convert_ns(self, t): 
        s,ns = divmod(t, 1000000000)
        m,s = divmod(s, 60)

        if m < 60:
           return "%02i:%02i" %(m,s)
        else:
           h,m = divmod(m, 60)
           return "%i:%02i:%02i" %(h,m,s)
    def ekpls(self,filename):        
        treeselection = self.treeview.get_selection()     
        self.treestore.clear()
        self.liste.clear()
        file_ = open(filename ).read().splitlines()
        file_list= [re.sub(r'file.*.=', '', x, flags=re.IGNORECASE).replace("file://","")  for x in file_]
        
     #       self.kal()
        for x in file_list:
           if os.path.isfile(x):
                name  = os.path.basename(x) 
                self.treestore.append(None,[name] )        
                self.liste[name] = x
        treeselection.select_path(0)
        treeselection.set_mode(gtk.SelectionMode.MULTIPLE)
        self.treeview.set_rubber_banding(True)
  #      self.oynat()                 
    def stop(self,data =None):
        self.player.set_state(gst.State.NULL) 
        self.time =  "00:00 / 00:00"
        self.sta.set_text(  self.time) 
        try:   gobject.source_remove(self.play_thread_id)           
        except:      pass         
        self.play_thread_id = None     
        self.pixbuf = './simgeler/rhythmbox-missing-artwork.svg'        
        self.iko(self.area,True)
 
        for x in self.info: x.set_text("")
        
        self.image.set_from_stock(gtk.STOCK_MEDIA_PLAY,3)    
        self.favo.set_value(0)       
        self.adj.set_value(0)
    def start_stop(self, filepath):     
        s_s =self.image.get_stock()[0]
        name = os.path.basename(filepath)
        if ".pls" in filepath:
           self.ekpls(filepath)
           return
        if  self.playing == filepath: 
           if s_s == "gtk-media-pause":
               self.image.set_from_stock(gtk.STOCK_MEDIA_PLAY,3)
               self.player.set_state(gst.State.PAUSED)
 
           else:
               self.image.set_from_stock(gtk.STOCK_MEDIA_PAUSE,3)
               self.player.set_state(gst.State.PLAYING)  
        elif os.path.isfile(filepath): 
 
            self.player.set_state(gst.State.NULL) 
            try:
                gobject.source_remove(self.play_thread_id)           
            except:
                pass 
            self.dur = None 
            self.image.set_from_stock(gtk.STOCK_MEDIA_PAUSE,3)                  
            self.player.set_property("uri", "file://" + filepath)    
            self.playing = filepath           
            self.player.set_state(gst.State.PLAYING)    
            self.play_thread_id = gobject.timeout_add(1000,self.play_thread)
            self.pixbuf ='./simgeler/rhythmbox-missing-artwork.svg'     
            self.iko(self.area,True)     
           
            self.tag.set_title(self.info[0],name,"b" )                    
            self.tag.set_title(self.info[1],"Bilimiyor","i" )                    
            self.tag.set_title(self.info[2],"Bilimiyor"  )                    
           
            if self.playing in self.view_list.sevilen.sections():
                val = self.view_list.sevilen._get(self.playing,"rating")
                self.favo.set_value(int(val ) )
            else:
                self.favo.set_value(0)        
    def station(self,uri ):
        self.player.set_state(gst.State.READY)           
        self.play_thread_id = None           
 
 
        self.pixbuf = uri[1]
        self.adj.set_value(0.0)        
        self.iko(self.area,True)     
        
        self.player.set_property("uri",uri[0])    
        
        self.image.set_from_stock(gtk.STOCK_MEDIA_STOP,3)    
        self.player.set_state(gst.State.PLAYING)  
 
    def progress(self):
        if self.i > 20:
            self.pro.hide()
            gobject.source_remove(self.ress)
            self.ress = None
            return False
        self.i += 1
        self.pro.pulse()
        return True
    def on_message(self, bus, message):
        t = message.type
 
        if t == gst.MessageType.BUFFERING:
            if   self.ress is None:
                self.pro.show()
                self.i = 0
                tx = "Ara Belleğe Alınıyor..."
                self.pro.set_text(tx) 
                self.pro.set_show_text(tx) 
                self.ress = gobject.timeout_add(100,self.progress)
 
        if t == gst.MessageType.EOS:
           self.stop()
        #       self.manager.add_item('file://' + self.playing)
           self.sonraki(True)    
        elif t == gst.MessageType.ERROR:
           self.stop()
           err, debug = message.parse_error()    
           try:
                self.sta.set_text("Hata: %s " % (err) ) 
           except:pass
        elif t == gst.MessageType.TAG:
            tags=message.parse_tag() 
            self.tag.system(tags)
            if self.tag.imgfile:
                self.pixbuf = self.tag.imgfile
                self.iko(self.area,True)
    def closex(self,w=False,data=False):        
        try:
            gobject.source_remove(self.play_thread_id)           
        except:    pass 
        gtk.main_quit()
    def on_sync_message(self, bus, message):
        print  (message.get_structure() )
        if message.get_structure().get_name() is None:return
        message_name = message.get_structure().get_name() 
        print (message_name)
        if message_name == "prepare-window-handle":
            gdk.threads_enter()
            gdk.Display.get_default().sync()
            imagesink = message.src 
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property('window').get_xid())
            gdk.threads_leave()
    
