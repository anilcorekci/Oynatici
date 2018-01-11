#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4

import pickle,os
class pick():
    def __init__(self,file_= None): 
        self.dizin = os.environ["HOME"].strip("\n")+"/"+".oynatıcı"
        if file_ is None:
            self.file = self.dizin +"/cache.pkl"
            self.al()
        else:       
            self.file = self.dizin + "/%s"  % (file_)
            if not os.path.isfile(self.file):
                os.system("> '{0}' ".format(self.file)  )
            self.al(True)
    def ek (self,dosya  ):
        if dosya in self.sozluk:
            return self.sozluk[dosya] 
        self.sozluk[dosya] = {}
        return  self.sozluk[dosya]
    def change(self,key,tag,value):    
        try:
            if type(value) is list:
                value = value[0]
            key[tag] = value
        except TypeError:
            return False        
 
        self.yaz()        
    def  get(self,key,tag):
        try:
            x = key[tag]
        except:
            return "Bilinmiyor"                        
        return x            
    def yaz(self,data=None):
        output = open(self.file, 'w')
        pickle.dump(self.sozluk, output)
        output.close()

    def al(self,dizelge=None):
        try:
            pkl_file = open(self.file, 'rb') 
        except IOError:
            self.sozluk = {}
            return 
        try:
            self.sozluk = pickle.load(pkl_file)
        except:
            self.sozluk = {}      

        pkl_file.close()
        if dizelge is None:
            for filename in  self.sozluk.keys():
                try:
                    if not os.path.isfile(filename):
                        del self.sozluk[x] 
                except:
                    continue                        
            self.yaz()
 

 
