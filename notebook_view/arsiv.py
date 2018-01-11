#! coding:utf-8 -*-
# vim: ts=8:sw=8

import  os
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
import  re,subprocess
 
import  time 

from widget import  bufferview,createbutton,createmenu,geticon  
 
home = os.environ["HOME"] 
 
class filesel(gtk.VBox ): 
    def __init__(self,player,tag=None,view_list=None):
        gtk.VBox.__init__(self)
        self.player = player
 
        self.current_directory = home
 
        self.get_icon = geticon.get_icon()                
 
        
        self.label = gtk.Label()
 

        self.label.set_alignment(0.01,0.50)        
        self.hbox = gtk.HBox(False,False)        
         
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_FIND,1)
     #   self.find =   gtk.ToggleButton( )
    #    self.find.add(image)
      #  self.find.set_flags(gtk.CAN_DEFAULT)
    #    self.find.set_focus_on_click(False) 
     #   self.find.set_relief(gtk.ReliefStyle.NONE)
    #    self.find.connect("toggled", self.ara)
 
 
        self.home = createbutton.rlb(gtk.STOCK_HOME,"Başlangıç",1,self.on_home_clicked)
        self.ekle =  createbutton.rlb(gtk.STOCK_ADD,"Ekle",1,self.ek)

        
        self.buffer = bufferview.buffer(self,home)

        self.hbox.pack_start(self.buffer.und  ,False,False,0)        
        self.hbox.pack_start(self.buffer.red ,False,False,0)
        self.hbox.pack_start(self.buffer.up,False,False,0)
                
        self.hbox.pack_start(self.home,False,False,0)
        self.hbox.pack_start(self.ekle,False,False,0)

        self.hbox.pack_start(self.label,False,False,2)
       # self.box = gtk.HBox(False,False) 
     #   self.entry =gtk.Entry()
      #  self.entry.connect("activate",self.bul)
      #  lab = gtk.Label("Ara: ")
      #  self.box.pack_start(lab,False,False,2) 
        #self.box.pack_start(self.entry,True,True,2) 
     #   self.hbox.pack_start(self.box,True,True,2)

        view = createbutton.rlb(  gtk.STOCK_JUSTIFY_FILL ,"",1,self.view) 
        listt = createbutton.rlb(gtk.STOCK_JUSTIFY_LEFT ,"",1,self.list)
        
        self.hbox.pack_end(listt,False,False,2)                                          
        self.hbox.pack_end(view,False,False,2 )                      
    #    self.hbox.pack_end(self.find,False,False,2) 
 
        self.pack_start(self.hbox, False, False, 2)
 

        self.dirIcon =  self.get_icon.diricon
 
        self.diricon =   self.get_icon.dirIcon
        self.fileIcon = self.render_icon(gtk.STOCK_FILE,5,None)
        self.get_icon.fileIcon = self.fileIcon
        self.sw = gtk.ScrolledWindow()
  #       self.sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
 
        self.pack_start(self.sw, True, True, 0)

        self.store = self.create_store()
        self.exper = [".png",".jpg",".bmp",".svg",".jpeg"]
 



        self.iconView = gtk.IconView()
        self.iconView.set_model(self.store)
        self.iconView.set_selection_mode(gtk.SelectionMode.MULTIPLE)
 
        self.menu = createmenu.menu(self.iconView )
        self.menu.add_item( gtk.STOCK_ADD, self.ek  )
        
        from notebook_view import progress 
        self.pr  = progress.progress(self,tag,view_list)
        self.arsv = self.menu.add_item("Belgeliğe Ekle",lambda w:self.pr.ekle() )        
        
        self.gizli = self.menu.add_item("Gizli Dosyalar" ,lambda w:self.fill_store() ,None,True)

        self.iconView.set_pixbuf_column(1)
        self.iconView.set_text_column(0)                     
    #    self.render_text =  self.iconView.get_cells()[1]
    #    self.render_text.set_fixed_height_from_font(1)

    #    self.render_text.set_property("single-paragraph-mode",True)

 #       self.render_text.set_property("wrap-mode",pango.WRAP_CHAR) 
   #     self.render_text.set_property("xalign",0.50)
  #      self.render_text.set_property("yalign",0.50)

        self.iconView.connect("item-activated", self.on_item_activated)
   #     self.iconView.set_cell_data_func(self.render_text, self.file_name) 
#
        self.iconView.connect_object("motion-notify-event",self.monotify,self.iconView)

        self.iconView.set_item_width(120)
        self.sw.add(self.iconView)
        self.iconView.grab_focus()
        
        self.cut = []
        self.cursor = {}

        self.data = None
 
        self.pixs =self.render_icon(gtk.STOCK_ADD,5,None)
        self.pix = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/mms.png",48,48)
  #      findview.findview(self.iconView)
 
        self.fill_store()
 
    def view(self,data):
        self.iconView.set_item_width(140)
       # self.render_text.set_property("xpad",3)
       # self.render_text.set_property("wrap-width",130)
        self.iconView.set_item_orientation(gtk.Orientation.VERTICAL)
    def list(self,data):
        self.iconView.set_item_width(-1)
    #    self.render_text.set_property("xpad",7)
   #     self.render_text.set_property("ypad",7)
  #      self.render_text.set_property("wrap-width",140)
        self.iconView.set_item_orientation(gtk.Orientation.HORIZONTAL)

    def monotify(self, iv, event) :

        pos = iv.get_path_at_pos(int(event.x), int(event.y))
        if pos: 
                data =  self.store[pos] [0]
                if  len(data) >= 28:
                        self.data =data 
 
                fil = self.current_directory+"/"+data
                if os.path.isfile(fil):
                        val = os.path.getmtime(fil)
                        son = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(val) )
                        boyut = os.path.getsize(fil)
                        tip= "\t<b>%s</b>\t\n\t<b>Son Değişim Tarihi: </b>%s\t\n\t<b>Dosya Boyutu:</b> %s Bayt\t" % (data,son,boyut)
                elif not os.path.isfile(fil):  
                        tip = "\t<b>%s</b>\t\n\n" %( data)                                 
                        try:    
                                z=0
                                for x in os.listdir(fil):   
                                        z+=1 
                                        if  filter(lambda i:i in x,self.exper) :
                                                continue
                                        tip = "%s \t%s"  % (tip,x+"\t\n")                 
                                        if z >10:break                        
                        except:return                

                else:tip = ""
                try:
                        self.iconView.set_tooltip_markup(tip.replace("&" ,"&amp;"))        
                except:return        
        else:
                self.iconView.set_tooltip_text("")                                                
                self.data =None
 

    def file_name(self, column, cell, model, iter):
        text =  model.get_value(iter, 0) 
        if self.data != text:
                try:
                        if  len(text) >= 28:
                                ctext = "%s%s" % (text[:26],"..")
                                self.cursor[ctext] = text
                        text = ctext
                except:
                        pass
        cell.set_fixed_size(-1,-1)
        cell.set_property('text', text)
        return

    def create_store(self):
        store = gtk.ListStore( str,gdkpixbuf.Pixbuf,bool)
        return store

    def fill_store(self):
        self.store.clear()
        #  self.find.set_active(False)
        if self.current_directory == None:
            return
        self.current_directory = self.current_directory.replace("/","\n")
        self.current_directory = self.current_directory.strip("\n")
        self.current_directory = self.current_directory.replace("\n","/")                   
        self.current_directory = "/" + self.current_directory  

        self.emit("dir-changed",self.current_directory)
        
        self.store.set_sort_column_id(2, gtk.SortType.DESCENDING) 
        self.label.set_text("Dosya Sistemi") 
        self.buffer.up.set_sensitive(False)
        if self.current_directory != "/":
                self.label.set_tooltip_text(self.current_directory)
                self.label.set_text(os.path.basename(self.current_directory))        
                self.buffer.up.set_sensitive(True)
        try:
                liste = os.listdir(self.current_directory)
                liste.sort(key=str.upper)
                for fl in liste:
                        if not self.gizli.get_active():
                                if fl[0] != ".":
                                        dosya = self.current_directory + "/" + fl 
                                        self.appendstore(dosya,fl)       
                        else:
                                dosya = self.current_directory + "/" + fl 
                                self.appendstore(dosya,fl)       
        except OSError :
                return
 
    def appendstore(self,dosya,fl):
 
        if os.path.isdir(os.path.join(self.current_directory, fl)):
                ln = None
                dr = self.current_directory+"/"+fl
                
                try: 

                        for x in os.listdir(dr):  
                                try:
                                        if os.path.isdir(dr+"/"+x): 
                                                for i in os.listdir(dr+"/"+x): 
                                                        if filter(lambda q:q in i,self.exper): 
                                                                ln = dr+"/"+x+"/"+i
                                                                break                                                                 
                                        else:
                                                if filter(lambda q:q in x,self.exper): 
                                                        ln = dr+"/"+x 
                                                        break       
                                except:pass                                                                                                                                                                                                     
                        if  ln :
                                try:
                                        icon = self.get_icon.get_pixbuf(ln,"folder1")
                                except:
               #                         print "Desteklenmiyen Simge %s" % (ln)
                                        icon = self.dirIcon
                                self.store.append([fl,icon,True])      
                                return        
                except:return          
                self.store.append([fl,self.dirIcon,True]) 
 
        else:                 
                try: 
                        if self.current_directory == "/":
                                raise IOError 
                except IOError  :                                
                        self.store.append([fl,self.get_icon.get_icon(dosya),False]) 
                        return
                pix = self.get_icon.get_thumb(dosya)
                self.store.append([fl,pix,False])   
 
    def ek(self,data=False):
        model = self.iconView.get_model()
        item = self.iconView.get_selected_items()
        
        for x in item:
                xname = None
                iter = model.get_iter(x)
                name = model[iter][0] 
                if name in self.player.liste:
                        continue
                filename = self.current_directory +"/" + name
                
                if os.path.isdir(filename):
                        self.player.dizin(filename) 
                        continue
                else:                
                        self.player.liste[name] = filename
                self.player.treestore.append(None, [name])
        self.iconView.unselect_all()                
        self.player.ek()                                                
    def on_home_clicked(self, widget):
        self.current_directory = home
        self.fill_store() 
    
    def on_item_activated(self, widget, item):
        self.iconView.set_tooltip_text("")                                                
        model = widget.get_model()
        path = model[item][0]
        file = self.current_directory +"/"+  path 
 
        if not os.path.isdir(file):
            os.system("xdg-open '"+file+"' 2> /dev/null")
            return

        self.current_directory = file
        self.fill_store()

 
    def ara(self,data):
 
        if data.get_active():
                self.box.show();self.label.hide()         
        else:
                self.box.hide();self.label.show()                 
    #   def bul(self,data):
    #       if self.entry.get_text() != "":     
        #           self.store.clear()       
    #   #               dosya = subprocess.Popen("find '"+self.current_directory+"'|grep -i '"+self.entry.get_text()+"'"  ,
           #                                               shell=True, stdout=subprocess.PIPE).communicate()[0]  
     #   #              dosya =  dosya.splitlines()
    #               for x in  dosya:          
    #                       fl = x.replace(self.current_directory+"/","")
     #                      self.appendstore(x,fl) 
    #               self.find.set_active(False)
 #  


gobject.type_register(filesel)
gobject.signal_new("dir-changed", filesel, gobject.SIGNAL_RUN_CLEANUP, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
 
