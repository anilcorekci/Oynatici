# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
import ConfigParser,os,shutil,re

class conf(ConfigParser.RawConfigParser):
    def __init__(self,confile):
        ConfigParser.RawConfigParser.__init__(self)

        self.path = confile
        self.readfp(open(self.path))

    def yaz(self,file=None): 
        with open(self.path, 'wb') as configfile:
            self.write(configfile)
    def set_conf(self,file,key=None,name=None): 
        if not file in self.sections():
            self.add_section(file)       
        if key and name:    
            if self._get(file,key) == name:
                return 
            self.set(file,key,name) 
            self.yaz(file)     
    def _get(self,file,key):
        try:
            val = self.get(file,key)
        except:
            if key == "title": return os.path.basename(file) 
            else:return "Bilinmiyor"
        else:return val    
    def get_conf(self,file):
        sozluk = { "title":self._get(file, 'title'),          
                 "album":self._get(file,'album'),
                 "artist":self._get(file,'artist'),
                 "image" :self._get(file,'image'),
                      }         
        return sozluk
    def _remove(self,x):
        try:
            self.remove_section(x)
        except KeyError:
            return
        self.yaz()     

