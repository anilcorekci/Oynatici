#! coding:utf-8 -*-
# vim: ts=4:sw=4
from gi.repository import Gst as gst
import os,mimetypes 
import hashlib 
from config import pick
 
#import pynotify
class tag():
    def __init__(self,player,info=None ):
        self.player = player
        self.info = info
        self.mesaj = None 
        self.imgfile = None
        self.pik = pick.pick()
        self.dizin = os.environ["HOME"].strip("\n")+"/"+".oynatıcı"
        self.progress = None
        
    def set_title(self,widget,title,sep="sub"):
    #tag adlı ayıklama dosyası hem progress hem de gui.py tarafından
    #kullanıldığı için sadece gui.py tarafından kullanılıyorsa 
    #yazı değiştirilmeli...
        if self.progress is True:
            return False
        if type(title) is list: title = title[0]
        title = title.replace("&","" )
        widget.set_tooltip_text( title  )                 
                
        if len(title) > 30:
            title = title[:27]+"..."
            
        widget.set_markup("<{1}>{0}</{1}>".format(title,sep) )                 
        widget.set_tooltip_text( title  )                 
        
    def system(self,tags,dizin=None,progress=None): 
        if progress is True:
            self.progress = True
        else:
            self.progress = None
            
        artist ="Bilinmiyor"; title="Bilinmiyor"; album = "Bilinmiyor" 
        if dizin:     path = dizin
        else:      
            try:                  

                path =  self.player.get_properties("uri")#.replace("file://","") 
                print path
            except AttributeError:
                return  False            
                
        self.imgfile = None
        song = self.pik.ek (path  )
        
        if tags.get_string("video-codec")[0]:	 
            self.pik.change(song,"video",True)     
        if tags.get_string("title")[0]: 
            title =  tags.get_string("title")[1]
            self.pik.change(song,"title",title)          
            if self.info and dizin is None: 
                self.set_title(self.info[0], title,"b"  )     
                                  
        if tags.get_string("genre")[0]:
            genre =  tags.get_string("genre")[1]
            self.pik.change(song,"genre",genre)           
            #print (genre)
 
        if tags.get_string("artist")[0]:   
            artist =  tags.get_string("artist")[1]
            #print (artist)
            self.pik.change(song,"artist",artist)
 

        if title is "Bilinmiyor":       
            title = os.path.basename(path)                    
            self.set_title(self.info[0], title, "b"  )      
                                           
        if self.info and dizin is None:  
            self.set_title(self.info[1], artist,"i" )     
                                              
        if tags.get_string("album")[0]: 
            album = tags.get_string("album")[1]
            #print (album)
            self.pik.change(song,"album",album)
            self.set_title(self.info[2], album )     


        #print dir(tags)
        #wiki.ubuntu.om/Novacut/Gstreamer1.0

        if tags.get_sample("image")[1]:  
            fil = str(artist)+"/"+str(album)+"/"+str(title)+"/"+str(path) 
            fil = hashlib.md5(fil).hexdigest() 
            file =  "%s/%s" %(self.dizin,fil) 
            
            buffer = tags.get_sample("image")[1].get_buffer()
            data = buffer.extract_dup(0,buffer.get_size() )
            
            if not os.path.isfile(file):
                try:
                    with open(file,"w") as png:
                        png.write(data)    
                except: return
                self.pik.change(song,"image",file)
                self.imgfile = file                        
            else:
                 self.imgfile = file                                                               
             #   if self.info:self.notify(artist,title,album,file)
    def notify(self, artist,title,album,file):
        if self.mesaj:self.mesaj.close()
        self.mesaj = pynotify.Notification(artist+"\n" +title+ " \n", album+"\nAlbümünden Söylüyor",   ( file))  
        try:self.mesaj.show()
        except:self.mesaj.close()                                
           
 
