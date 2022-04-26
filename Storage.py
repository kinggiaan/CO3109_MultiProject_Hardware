# class Storage:
machine_storage = [    {"name":"Dasani", "locate": 1, "qty": 0},
                       {"name":"NutriBoost", "locate": 2, "qty": 0},
                       {"name":"Sting", "locate": 3, "qty": 1},
                       {"name":"Black Coffee", "locate": 4, "qty": 10},
                       {"name":"Coca Cola", "locate": 5, "qty": 3},
                       {"name":"Coca Light", "locate": 6, "qty": 3}
                   ]


# Return information
def Product_find(self, name ):
    for storage in machine_storage:
        if storage["name"] == name:
            return storage

#Quantitive Function
def Qty_find(self, name ):
    for storage in machine_storage:
        if storage["name"] == name:
            return storage["qty"]

def Qty_update(self,name,n_qty):
    for storage in machine_storage:
        if storage["name"] == name:
            storage["qty"] = n_qty

def Qty_realese(self, name,qty):
    for storage in machine_storage:
        if storage["name"] == name:
            storage["qty"] -= qty
#Locate Function

def Locate_find(seft, name):
    for storage in machine_storage:
        if storage["name"] == name:
            return storage["locate"]

def Locate_update(self,name,n_locate):
    for storage in machine_storage:
        if storage["name"] == name:
            storage["qty"] = n_locate

#Product function
def Prod_add(seft, n_name,n_locate,n_qty):
    n_product = [{"name":n_name, "locate": n_locate, "qty": n_qty}]
    machine_storage.append(n_product)

def Prod_delete(seft,name):
    for storage in machine_storage:
        if storage["name"] == name:
            machine_storage.remove(seft,storage)
