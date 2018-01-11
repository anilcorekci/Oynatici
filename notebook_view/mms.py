#! coding:utf-8 -*-
# vim: ts=4:sw=4
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
from gi.repository import Gdk  as gdk 
import  os
from config import conf
from widget import geticon
cfg = os.environ["HOME"].strip("\n")+"/"+".oynatıcı/mms.cfg"


class filesel(gtk.VBox ): 
    def __init__(self):
        gtk.VBox.__init__(self)
        self.config = conf.conf(cfg)
        self.geticon = geticon.get_icon()
        
        self.toolbar = gtk.Toolbar()
        self.toolbar.set_style(gtk.ToolbarStyle.BOTH_HORIZ)
        self.pack_start(self.toolbar, False, False, 0)
        self.item( gtk.STOCK_MEDIA_PLAY, self.oynat)
        self.item( gtk.STOCK_ADD, self.yeni)
        self.item( gtk.STOCK_EDIT, self.add)        
#              self.item( gtk.STOCK_REFRESH,self.refresh)  
        self.item( gtk.STOCK_REMOVE,self.remove)  
    
        self.sw = gtk.ScrolledWindow()
     #    self.sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
 
        self.pack_start(self.sw, True, True, 0)
        self.store = self.create_store() 
        
        self.iconView = gtk.IconView() 
        self.iconView.set_model(self.store)
        self.iconView.set_text_column(0)
        self.iconView.set_pixbuf_column(1)
        self.iconView.set_item_width(90)
        
        self.sozluk ={}
 
        self.sw.add(self.iconView)
        self.iconView.grab_focus()
        self.pix = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/mms.png",80,80)
        self.refresh()                

    def item(self,stock,kontak):
        item = gtk.ToolButton()
        item.set_icon_name(stock)
        item.set_is_important(True)        
        item.connect("clicked", kontak)
        self.toolbar.insert(item, -1)                  
    def create_store(self):
        store = gtk.ListStore(str, gdkpixbuf.Pixbuf, bool)
        store.set_sort_column_id(0, gtk.SortType.ASCENDING)
        return store
    def oynat(self,data=None):
        model = self.iconView.get_model()
        item = self.iconView.get_selected_items()
        tag  = None
        for x in item:
            iter = model.get_iter(x) 
            tag = model[iter][0]
        if not tag is None:
            path = self.sozluk[tag]
            self.station(path )
    def refresh(self,data=None):
        self.store.clear() 
        for x in self.config.sections():
            n1 =self.config._get(x,"title")
            n2 =self.config._get(x,"image")
            self.sozluk[x] = n1,n2 
            self.store.append([ x, self.get_image(n2), True])                 
    def get_image(self,file_):
        if file_ != "Bilinmiyor":

                try:
                    px  = self.geticon.get_pixbuf(file_)
                except: return self.pix            
                return px               
        else:  return self.pix              
    def update_preview_cb(self,file_chooser, preview):
        filename = file_chooser.get_preview_filename()
        try:
                pixbuf = gdkpixbuf.Pixbuf.new_from_file_at_size(filename, 128, 128)
                preview.set_from_pixbuf(pixbuf)
                have_preview = True
        except:
                have_preview = False
        file_chooser.set_preview_widget_active(have_preview)
        return             
    def set_image(self,data,label,image):
        dialog = gtk.FileChooserDialog("Simge Dosyası Seç..",
                                                                None,
                                                                gtk.FileChooserAction.OPEN,
                                                               (gtk.STOCK_CANCEL,gtk.ResponseType.CANCEL,
                                                                gtk.STOCK_OK, gtk.ResponseType.OK))        
        dialog.set_default_response(gtk.ResponseType.OK)
        preview = gtk.Image()

        dialog.set_preview_widget(preview)
        dialog.connect("update-preview", self.update_preview_cb, preview) 
 
        x = gtk.FileFilter()
        x.set_name("Resimler")
        [x.add_pattern("*%s" %(i) )  for i in ["png","jpg","JPEG","jpeg","bmp"] ]
        dialog.add_filter(x)
        
 
        if dialog.run()    == gtk.ResponseType.OK:     
                info = dialog.get_filename()
                label.set_text(os.path.basename(info ) )                
                label.set_tooltip_text(info)
                image.set_from_pixbuf(self.get_image(info) )
        dialog.destroy()          
        del dialog,preview                                 
    def dialog(self,data=None):
        builder = gtk.Builder()
        builder.add_from_file("./glade/dialog.glade")
        en = builder.get_object("entry1")
        en1 =builder.get_object("entry2")
        image = builder.get_object("image1")
        filecho = builder.get_object("label3")
        button = builder.get_object("button3")
        button.connect("clicked",self.set_image,filecho,image)
        w=builder.get_object("dialog1")

        if data:
                for x in self.item:
                        iter = self.model.get_iter(x)
                        path = self.model[iter][0]
                en.set_text(path)
                en1.set_text(self.sozluk[path][0] )        
                imfile = self.sozluk[path][1]
                image.set_from_pixbuf(self.get_image(self.sozluk[path][1] )   )
                filecho.set_text(os.path.basename(imfile) ) 
                filecho.set_tooltip_text(imfile)
        if builder.get_object("dialog1").run() == 1:
                return en,en1,image,filecho,w
        else:
                w.destroy()
                return False
    def add(self,data=None):
        self.model = self.iconView.get_model()
        self.item = self.iconView.get_selected_items()

        if bool(self.item): 
                try:                
                        en,en1,image,filecho ,w  =self.dialog(True)
                except:return
        else:return                
        n,n1=en.get_text(),en1.get_text()
        self.sozluk[n] = n1 ,filecho.get_tooltip_text()
        self.config.set_conf(n,"title",n1)
        self.config.set_conf(n,"image",filecho.get_tooltip_text())
        w.destroy() 
        self.refresh()                        
    def yeni(self,data): 
        try:
                    en,en1,image,filecho,w =self.dialog()
        except :return                  
        n,n1=en.get_text(),en1.get_text()
        self.sozluk[n] = n1,filecho.get_tooltip_text()
        self.store.append([ n, self.pix, True])         
        self.config.set_conf(n,"title",n1)
        self.config.set_conf(n,"image",filecho.get_tooltip_text())                  
        w.destroy()                     
        self.refresh()                             
 

    def remove(self,data=None):
        model = self.iconView.get_model()
        item = self.iconView.get_selected_items()
        for x in item:
                iter = model.get_iter(x)
                path = model[iter][0]
                self.config.remove_section(path)
                self.config.yaz()
                model.remove(iter)

