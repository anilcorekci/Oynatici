# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
from gi.repository import Gdk as gdk
import  os
from widget import  (
    createmenu,
    createbutton,
    findview,
    geticon ,
    remover )
from config import  conf,pick

svcfg = os.environ["HOME"].strip("\n")+"/"+".oynatıcı/"+"favori.cfg"
if not os.path.isfile(svcfg):
    os.system("> '%s' "%(svcfg))

class hbox(gtk.VBox):
    def __init__(self,player,pik):
        gtk.VBox.__init__(self)
        self.player = player
        self.pick =  pik
        self.dizi =  ["İzleti","♥♥♥♥♥","Dinleti","Sevilenler","Bilinmiyor","Çalma Dizelgeleri"]
        self.xlisstore = []
        
        self.dizelge = pick.pick("dizelge.pkl")
        
        self.svcfg = svcfg
        self.sevilen = conf.conf(self.svcfg)
        self.player.favo.connect("rating-changed",self.favor)  
        self.sozluk = self.pick.sozluk
        self.val = 0
        self.set_border_width(7)
        self.geticon = geticon.get_icon()

    
        self.en = gtk.Entry()        
        self.en.set_size_request(180,-1)
        self.en.set_placeholder_text("Aramak için yazın..")
        self.en.set_icon_from_stock(1, gtk.STOCK_CLEAR)
        self.en.connect("changed",self.enpress)
        self.en.connect("icon-press",self.refresh)


        self.liststore = gtk.ListStore(str) 
        self.completion = gtk.EntryCompletion() 
        self.completion.set_model(self.liststore)
        self.en.set_completion(self.completion)
        self.completion.set_text_column(0)

        self.hbox = gtk.HBox() 
 
        arama  = createbutton.toggle("./simgeler/folder.png","","Album") 
        arama.set_active(True) 
        arama.connect("toggled",self.tog) 

 
        self.info = gtk.Label()
        
        bx = gtk.HBox()
        sanat = createbutton.toggle( "audio-x-generic","Akım Dizisi")
        sanat.connect("toggled",self.sanat)
        bx.pack_end(self.en ,False,False,0 )
        bx.pack_start(sanat ,False,False,3)
        
        self.hbox.pack_start(bx,False,False,3)
        self.hbox.pack_start( arama,False,False,6)
        self.hbox.pack_end(self.info,False,False,2)
        self.hbox.set_border_width(3)
        
 
        self.pack_start(self.player.ev_style(self.hbox),False,False,12)

        self.treestore = gtk.TreeStore(str)
        self.treestore.set_sort_column_id(0, gtk.SortType.ASCENDING)
        
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.set_headers_clickable(True)       
        self.cell = gtk.CellRendererText()          
        self.cell.set_property( 'editable', True )
        self.cell.connect( 'edited', self.col0_edited_cb, self.treestore )
 
                
        self.tvcolumn = gtk.TreeViewColumn(" ",  self.cell ) 
        self.tvcolumn.set_cell_data_func(self.cell, self.file_name)
        self.treeview.append_column( self.tvcolumn)
        self.treeview.connect("motion-notify-event",self.monoti)        
        self.treeview.set_headers_visible(False) 
        
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(True,True)
        self.sw.add(self.treeview )
        self.sw.set_size_request(220,-1)
        self.treeview.connect("cursor-changed",self.active)

        self.treeview.set_headers_clickable(True)
        self.treeview.set_headers_visible(False)

        self.treeview.set_rules_hint(True)
        
        self.store1 = self.create_store() 
        self.sw1,self.iconView1 = self.create_view(self.store1,gtk.SelectionMode.MULTIPLE)
       #  self.iconView1.connect_object("motion-notify-event",self.monotify,self.iconView1)
	
        self.sevimge = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/star.svg",40,40)
        self.fileIcon  = self.geticon.fileIcon 
        
 
        hbox = gtk.HBox()
        hbox.pack_start(self.sw,False,False,6)
        

        
        self.dirIcon = self.geticon.belgelik
        self.dizicon = self.geticon.dizelge
        
        self.store = self.create_store() 
        self.alsw ,self.iconView = self.create_view(self.store,gtk.SelectionMode.MULTIPLE)
        self.alsw.set_policy( gtk.PolicyType.AUTOMATIC,gtk.PolicyType.NEVER)
        self.alsw.set_size_request(True,True)
        self.iconView.connect("selection-changed",self.ekle)           
        self.iconView.connect("scroll-event",self.swpress,self.alsw)
        self.iconView.connect("motion-notify-event",self.simgefaresi,self.alsw) 
    #    self.iconView.set_text_column(1)
        self.iconView.set_columns(100)


        self.iconView.set_pixbuf_column(1)
        vbox = gtk.VBox()
        vbox.pack_start(self.alsw,False,False,0 )
        
      #  self.sw1.set_size_request(200,180)
        self.sep = gtk.HSeparator()
        vbox.pack_start(self.sep,False,False,0)     
        vbox.pack_end(self.sw1,True,True,0)



        self.refresh()    


     #    self.buton = gtk.Button("Ekle")
        #buton.connect("clicked",self.ek)            
       
        hbox.pack_end(vbox,True,True,0)
        self.pack_end(hbox,True,True,0)
       #    findview(self.iconView)
        #  self.pack_end(self.buton,False,False)

        from widget import tooltipview
        self.tool = tooltipview.tooltipview(self.iconView1,self)
      
        find = findview.findview(self.iconView1)
 
        
        self.menu =  createmenu.menu(self.iconView1,3)#,self.tool)
        self.menu.add_item( gtk.STOCK_ADD, self.ek )
        self.menu.add_item(gtk.STOCK_DELETE,self.remove,"title")
 
        self.menu =  createmenu.menu(self.iconView)
        self.menu.add_item( gtk.STOCK_ADD, self.ek1 )
        self.menu.add_item(gtk.STOCK_DELETE,self.remove,"album")
        
        self.menu =  createmenu.menu(self.treeview)
        self.menu.add_item( gtk.STOCK_ADD, self.ek2 )        
        self.menu.add_item(gtk.STOCK_DELETE,self.remove,"artist")
        
        self.gezgin = ""
 
 
    def monoti(self,w,event):
        try:
            kord = w.get_path_at_pos(int(event.x) , int(event.y) )[0]
        except:
            self.gezgin = ""
        else:
            self.gezgin =  w.get_model()[kord] [0]
    def tog(self,data):  
        """ göz at için gtk arac dizisini göster/gizle"""
        if data.get_active():
            self.alsw.show() ;  self.sep.show()  
        else:
            self.alsw.hide() ;  self.sep.hide()   
    def sanat(self,data):
        if data.get_active(): self.sw.hide();self.en.hide()    
        else: self.sw.show()   ;self.en.show()          
 
    def favor(self,data=None,x=None): 
        self.sevilen.set_conf(self.player.playing,"rating",x) 
        del self.sevilen
        self.sevilen = conf.conf(svcfg)
    def simgefaresi(self,widget,event,sw):        
        adj = sw.get_property("hadjustment")
        val = adj.get_value()
        h = sw.get_allocation().width
        upper = adj. get_property("upper")
        adimm = 3
        if h == upper:  return
        if  event.x  >  (h+self.val) - 60:   
            if event.x >= upper :
                return         
            adj.set_value(val +adimm  )
            self.val+=adimm
        if event.x  <   val+ 60   :
            if event.x <= 0:
                return
            adj.set_value(val- adimm )    
            self.val -= adimm
 
    def swpress(self,widget,event,sw):
 
        adj = sw.get_property("hadjustment")
        val = adj.get_value()   
        h = sw.get_allocation().width
        upper = adj. get_property("upper")
        
        if h == upper:  return
        
        if event.direction == gdk.ScrollDirection.UP:
            if event.x >=  upper  :
                return
            nval = val + 10 
            adj.set_value( nval )
        if  event.direction == gdk.ScrollDirection.DOWN:
            nval  = val - 10
            if nval <  0:
                return
            adj.set_value( nval  )        
                        

    def file_name(self, column, cell, model, iter,xx):
     
        text =  model.get_value(iter, 0) 
        cell.set_property('text', text)
        
        cell.set_property('scale', 1.0)
        
        if text == self.gezgin:
            cell.set_property('scale', 1.2500) 
 
        
        if len(text) >= 27:
            self.treeview.set_tooltip_text(text)
        else:
            self.treeview.set_tooltip_text("")
        return
 
    def col0_edited_cb( self, cell, path, new_text, model ):   
        ar = "artist"
        ex_text =   model[path][0]  
        if ex_text == new_text or ex_text in self.dizi:
            return
        ne = model[path].get_parent()[0]
 
        if ne == "Çalma Dizelgeleri":        
            if ex_text != new_text:  
                liste = self.dizelge.sozluk[ex_text]
                if new_text in self.dizelge.sozluk:
                    xliste = self.dizelge.sozluk[new_text]
                    liste = xliste + liste
                self.dizelge.sozluk[new_text] = liste
                del self.dizelge.sozluk[ex_text]
                self.dizelge.yaz()
                self.check_list(self.sozluk)
            return                 
        if new_text in  [self.get_value(y,ar)  for y in self.sozluk]:
            iter = model.get_iter(path)
            model.remove(iter)
        
        else:
            model[path][0] = new_text 
        if ex_text != new_text: 
            for x in filter(lambda i: ex_text == self.get_value(i,ar),self.sozluk):
                self.pick.change(self.pick.ek(x),ar,new_text)
                mutagen_meta.set_tag(x,ar,new_text )                          
        return
    def create_view(self,store,multi=gtk.SelectionMode.SINGLE):
        iconView = gtk.IconView()
        iconView.set_model(store)
        iconView.set_pixbuf_column(1)
        iconView.set_text_column(0)         
        iconView.set_item_width(140)     
        iconView.set_selection_mode(multi)
        sw = gtk.ScrolledWindow()         
        sw.set_policy( gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        sw.add( iconView)
        return sw,iconView

    def create_store(self):
        store = gtk.ListStore( str,gdkpixbuf.Pixbuf,bool)
        store.set_sort_column_id(0, gtk.SortType.ASCENDING)
        return store        
    def ek12(self,x):
            try:
                parent = self.sozluk[ x]["title"]    
            except KeyError:
                parent = os.path.basename( x)     
            if parent in self.player.liste:
                    return
            self.player.liste[parent] = x
            self.player.treestore.append(None, [parent])        
    def get_artist_files(self,dizelge=None):
        treeselection = self.treeview.get_selection()
        (model, rows) = treeselection.get_selected_rows()
        artist_files = []
        for x in rows:
            try:iter = model.get_iter(x)
            except ValueError:continue
            name = model[iter][0]    
            if not dizelge is None:
                if name in self.dizelge.sozluk: 
                    del self.dizelge.sozluk[name]
                    self.dizelge.yaz()     
                    continue                           
            [artist_files.append(y) for y in filter(lambda i: name == self.get_value(i,"artist"),self.sozluk) ]
        return artist_files     
    def get_album_files(self):
        model = self.iconView.get_model()
        item = self.iconView.get_selected_items() 
        album_files = []
        for x in item:
            iter = model.get_iter(x)
            name = model[iter][0] 
            [album_files.append(y ) for y in filter(lambda i:self.bilgi == self.get_value(i,"artist") and \
                                                             self.get_value(i,"album") == name,self.sozluk )]                        
        return album_files              
    def get_title_files(self):
        model = self.iconView1.get_model()
        item = self.iconView1.get_selected_items()
        title_files = []
        for x in item:
            iter = model.get_iter(x)
            name = model[iter][0] 
            xname = unicode(name,"utf-8")                                                       
            try:
                filename = self.song[name]  
            except KeyError:
                filename = self.song[xname]
            title_files.append(filename)                
        return title_files      
 
    def remove(self,widget,data):
        if data == "album":
            for x in self.get_album_files():
                if x in self.bilinmiyor_artist: continue
                del self.sozluk[x] 
            remover.remove_iconview(self.iconView )                           
        if data == "artist":                             
            for x in self.get_artist_files(self.dizelge): 
                if x in self.bilinmiyor_artist: continue
                else:
                    del self.sozluk[x] 
            remover.remove_treeview(self.treeview,self.dizi)                
        if data == "title":  
            try:
                liste = self.dizelge.sozluk[self.bilgi]
            except KeyError:
                liste = []
            for x in self.get_title_files():
                if x in liste:
                    liste.remove(x)
                    self.dizelge.yaz()
                elif  x in self.sevilen.sections():
                    self.sevilen._remove(x)  
                    del self.sevilen
                    self.sevilen = conf(svcfg)  
                else:
                    try:
                        del self.sozluk[x]             
                    except KeyError:
                        print "Key Error:{0}".format(x)
                        return False                        
            remover.remove_iconview(self.iconView1)                    
        self.pick.yaz()

    def ek2(self,data):
        for x in self.get_artist_files():self.ek12(x) 
        self.player.ek()                
    def ek1(self,data=None):
        for x in self.get_album_files() :self.ek12(x) 
        self.player.ek()         
    def ek(self,data=None):
        for x in self.get_title_files():self.ek12(x)  
        self.player.ek()                 

    def refresh(self,widget=None,iconpos=None,event=None): 
        self.check_list(self.sozluk)
        if iconpos and event:
            widget.set_text("")
    def get_value(self,eleman,ne):
        try:
            return self.sozluk[eleman][ne] .encode('utf-8')
        except KeyError: 
            return "Bilinmiyor"         
        except AttributeError:
            return self.sozluk[eleman][ne]
        except UnicodeDecodeError:
            return self.sozluk[eleman][ne].decode('utf-8').encode('utf-8')
    def enpress(self,w ):  	
 
 
        text = w.get_text() 
        if  len(text) <= 0:
            self.check_list(self.sozluk)           
            return
 
        sozluk = []
        for x in  self.sozluk:
            arg = self.get_value(x,"title"),self.get_value(x,"album"),self.get_value(x,"artist")
            if text in arg or text in x:
                 sozluk.append(x)                            
        self.check_list(sozluk)           

    def check_list(self,data=None):        
    
        self.treestore.clear()
 
        self.video = self.treestore.append(None,["İzleti"])       
        self.music =  self.treestore.append(None,["Dinleti"])            
        self.sevilenler = self.treestore.append(None,["Sevilenler"])  
        self.xmusic =  self.treestore.append(self.video,["Bilinmiyor"])      
        self.xvideo =  self.treestore.append(self.music,["Bilinmiyor"])         
        self.calma =  self.treestore.append(None,["Çalma Dizelgeleri"])     

                     
        for x in self.dizelge.sozluk:
            self.treestore.append(self.calma,[x])                   
            
        self.bilinmiyor_artist = []
        eklenen = []

        
        for x in data :
            title = self.get_value(x,"artist") 
            try:
                y = os.path.basename(os.path.dirname(x) )
            except AttributeError:
                continue                    
            if not  y in self.xlisstore:
                self.liststore.append([y])  
                self.xlisstore.append( y )   
                
            if title == "Bilinmiyor":
                self.bilinmiyor_artist.append(x)
                continue     


                                     
            if  title in eklenen: continue                  
            if self.get_value(x,"video") == True:               
                self.treestore.append(self.video,[title])
            else:
                self.treestore.append(self.music,[title])               
            if  title in eklenen: continue       
            eklenen.append(title)               
            if not  title in self.xlisstore:
                self.liststore.append([title])   
                self.xlisstore.append( title )   
 
        treeselection = self.treeview.get_selection() 
        treeselection.set_mode(gtk.SelectionMode.MULTIPLE)
        self.treeview.set_rubber_banding(True)
        self.treeview.expand_all()
        del eklenen  
 
 
    def artist_eklenen(self,album,artist):

        if  not album in self.eklenen:
            self.eklenen[album] = []            
            self.eklenen[album].append(artist)
      #      print artist
        else:
            if not artist in self.eklenen[album]:
                self.eklenen[album].append(artist)
            
    def active(self,data=None):
        treeselection = self.treeview.get_selection() 
        (model, rows) = treeselection.get_selected_rows()
        
        self.val = 0    
        self.store.clear()            

        self.eklenen = {}
        for x in rows:
            try:iter = model.get_iter(x)
            except ValueError:continue
 
            name = model[iter][0]
            path = model.get_path(iter)
            if not name in "Sevilenler":
                try:
                    self.ne =   model[path].get_parent()[0]
                except TypeError:
                    continue
            parent = name  

            self.bilgi = parent

            try:len(parent)
            except:return
            if parent == "Bilinmiyor":
                for x in self.bilinmiyor_artist:                               

                    album = self.get_value(x,"album")
                    if album in self.eklenen:                   
                        self.artist_eklenen(album, self.bilgi )                  
                        continue  
                    if self.ne == "İzleti":
                        if self.get_value(x,"video") == True: 
                            self.album_ekle(x,album)

                    else:                
                        if self.get_value(x,"video")  != True:
                            self.album_ekle(x,album)
 
            else:
                for x in filter(lambda i:self.get_value(i,"artist") == parent,self.sozluk): 
             
                    album =  self.get_value(x,"album") 
                    if album in self.eklenen:                   
                        self.artist_eklenen(album, self.bilgi )                  
                        continue  
                    self.album_ekle(x,album) 
 
 
            if name in self.dizelge.sozluk:                    
                if name in self.eklenen: continue             
                self.store.append([  name  ,self.dizicon, False]) 	          
                self.artist_eklenen(name, self.bilgi )                  
            if name in "Sevilenler":
                if name in self.eklenen: continue             
                for i in range(1,6):self.store.append(["%s" %("♥" * i),self.sevimge,False])      
                self.bilgi = "♥"                  
                self.artist_eklenen(name, self.bilgi )                  

            self.iconView.select_all()                             
 

 
        
    def album_ekle(self,x,album):
 
        self.artist_eklenen(album, self.bilgi )                  
        pixbuf = self.dirIcon            
        
        if self.get_value(x,"video") == True:   
            try:
                thumb = self.geticon.get_thumb_file(x)
                pixbuf = self.geticon.get_pixbuf( thumb)   
            except:pass
        else:
            pix =  self.get_value(x,"image")
            try:
                pixbuf = self.geticon.get_pixbuf(pix)    
            except:pass

        
        self.store.append([ album,pixbuf, False]) 	                
               
    def store_ekle(self,filename): 
        try:
            parent = self.sozluk[ filename]["title"]    
        except KeyError:
            parent = os.path.basename( filename)
            
        if parent in self.song and self.song[parent] == filename:
            return False
            
        self.song[parent] = filename          
        self.store1.append([parent,self.geticon.get_thumb(filename),False])                     
        return parent      
    def title_ayikla(self,album,bilgi):
    
        if bilgi in self.dizelge.sozluk: 
            for x in self.dizelge.sozluk[ bilgi]:  self.store_ekle(x)  
                    
        elif bilgi in "♥♥♥♥♥":
            for x in self.sevilen.sections():
                if  self.sevilen._get(x,"rating") == "%s" %(len(album ) / 3 ): self.store_ekle(x)  
                        
        elif  bilgi == "Bilinmiyor":
            for x in filter(lambda i:self.get_value(i,"album") == album,self.bilinmiyor_artist):   
                if self.ne == "İzleti" and self.get_value(x,"video") == True:    self.store_ekle(x) 
                if self.ne == "Dinleti" and self.get_value(x,"video") != True:   self.store_ekle(x)  
                        
        else:
            for x in filter(lambda x: bilgi == self.get_value(x,"artist") and\
                album == self.get_value(x,"album")  ,self.sozluk):  self.store_ekle(x)               
                
    def ekle(self,data=None):
        self.store1.clear()
        self.song = {}  
        self.burdan = 0
        self. miktar = len(data.get_selected_items() ) 
        if  self.miktar >= 20:
            self.ayir =  self.miktar / 10
            self.player.pro.show()
        else:
            self.ayir =  self.miktar      
        self.id = gobject.timeout_add(50,self.ekle_,data)
        
    def ekle_(self,data):
        
        items = data.get_selected_items() [self.burdan:self.ayir]
        
        for x in   items:
            model = data.get_model()
            i = model.get_iter(x)     
            album = model[i][0]  
            
            if album in "♥♥♥♥♥":
                self.title_ayikla(album, "♥")
                continue
            try:
                artist_list = self.eklenen[ album ] 
            except KeyError:
                artist_list = self.eklenen[ unicode(album,"utf-8") ] 
            for x in  artist_list: 
                self.title_ayikla(album,x)
            self.burdan += 1
            if self.burdan == self.ayir and self.miktar >= 20:
                self.ayir += self.ayir
                self.player.pro.pulse()
                return True
        try:                
            gobject.source_remove(self.id)
        except ValueError:
            del self.id
        self.player.pro.hide()
        self.info.set_text("  {0} albüm {1} şarkı..\t".format( self.miktar, len(self.song   ) ) )

