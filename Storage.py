# class Storage:
machine_storage = [{"name":"Drink 1", "locate": 1, "qty": 2},
                       {"name":"Drink 2", "locate": 2, "qty": 0},
                       {"name":"Drink 3", "locate": 3, "qty": 1}]
def find_Qty(self, name ):
    for storage in machine_storage:
        if storage["name"] == name:
            return storage["quantitive"]