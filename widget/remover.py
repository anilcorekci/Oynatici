# -*- coding: utf-8 -*- 
# vim: ts=4:sw=4
def remove_treeview(treeview,dizelge=None):
        treeselection =  treeview.get_selection()
        (model, rows) = treeselection.get_selected_rows()
 
        for x in rows:
            try:iter = model.get_iter(x)
            except ValueError:remove_treeview(treeview);return             
            name = model[iter][0]  
            if name in  dizelge:
                continue
            model.remove(iter)  
 
def remove_iconview(iconview):
    model = iconview.get_model()
    item = iconview.get_selected_items() 
    for x in item:
        iter = model.get_iter(x) 
        model.remove(iter)
 
