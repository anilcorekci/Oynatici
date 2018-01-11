# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
from gi.repository import Gio as gio
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkpixbuf
import os
import mimetypes
from PIL import Image, ImageOps
import StringIO
import urllib,hashlib
class get_icon():
    def __init__(self): 
        self.diricon = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/folder_.png",80, 80)
        self.belgelik = gdkpixbuf.Pixbuf.new_from_file_at_size("./simgeler/folder.png",80, 80) 

        self.icontheme = gtk.IconTheme.get_default()   
        
        self.dizelge = self.themeicon( "audio/x-scpls",40)                
        self.fileIcon  = self.themeicon("audio-x-generic",40)
        self.fileIcon1  = self.themeicon("image-x-generic",40)
        self.dirIcon =  self.themeicon("folder",48)
        
    def themeicon(self,name,size):
        """Eğer mimetype  simge barındırıyorsa gönder
        barındırmıyorsa False değer ver"""
        gicon = gio.content_type_get_icon (name)  
        iconinfo = self.icontheme.choose_icon(gicon.get_names(),size, gtk.IconLookupFlags.USE_BUILTIN)
        if iconinfo:
            return iconinfo.load_icon()
        else:
            return False                
    def get_icon(self, name):
        """dosyanın mimetype 'i simgeyse gönder değilse
        tanımlanan simgeyi gönder"""    
        try:
            types = mimetypes.guess_type(name) [0]
            if   self.themeicon(types,40): 
                return self.themeicon(types,40)       
            else:
                return self.fileIcon                             
        except:
            return self.fileIcon        
    def get_thumb_file(self,file_):
        """gnome için thumb dizininden simgeyi 
        md5 ile dosya yolundan bul"""
        try:op = urllib.urlopen(file_)
        except IOError (err):
            print (err)
            return self.fileIcon1
        fl = op.geturl() 
        fil = hashlib.md5(fl).hexdigest()          
        return  os.environ["HOME"]+"/.thumbnails/normal/"+fil + ".png"     
    def get_thumb(self,file_):
        """dosya için thumb simgesi ara"""  
        """ Yeni gnome yapılandırmalarında .thumbnails dizini eski\
        mantıkla çalışmıyor tüm dosyalar için bir referans noktası değil??"""
        try:
            pix = gdkpixbuf.Pixbuf.new_from_file_at_size( self.get_thumb_file(file_),80, 80)
            return pix
        except Exception:
            return self.get_icon(file_)
    def get_pixbuf(self,image, shape = "cover"):
        """get_pixbuf _ dosya yolu , maske
        PIL ile maske ile yeni bir pixbuf gönder"""
        
        iconPath = image 
        highlight = Image.open('simgeler/%s.png' % shape)
        mask = Image.open('simgeler/%s-mask.png' % shape) 
        icon = Image.open(iconPath).convert('RGBA')#.rotate(-6)  
        button = Image.new('RGBA', mask.size) 
        icon = ImageOps.fit(   icon, highlight.size, method=Image.ANTIALIAS, centering=(0.5,0)    ) 
        helper = button.copy() 
        helper.paste(icon, mask=mask) 
        button.paste((255, 255, 255), mask=mask) 
        icon = icon.convert('RGB') 
        button.paste(icon, mask=helper) 
        overlay = highlight.copy().convert('RGB') 
        button.paste(overlay, mask=highlight)
        file1 = StringIO.StringIO()   
        button.save(        file1, "png")  
        contents = file1.getvalue()  
        file1.close()  
        loader = gdkpixbuf.PixbufLoader()  
        loader.set_size(80, 80)
        loader.write(contents )  
        pixbuf = loader.get_pixbuf()  
 
        loader.close()  
        return pixbuf  
                
