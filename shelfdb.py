import shelve

class ShelfDB (object):
    def __init__(self, dao_type, model_info=None, prefix='shelfdb', id_key='shelfid', is_rawdata=False):
        # TODO: assert dao_model exists in dao_type 
        self.db = shelve.open(prefix)
        self.id_key = id_key
        self.is_rawdata = is_rawdata
        self.dao_type = dao_type
        self.model_info = model_info if model_info else dao_type.dao_model()
    
    def close(self):
        self.db.close()
    
    def save(self, data):
        if isinstance(data, dict):
            key = data[self.id_key]
            if self.is_rawdata:
                self.db[key] = data
            else:
                self.db[key] = self.dao_type(**data)
        elif isinstance(data, self.dao_type):
            self.db[getattr(data, self.id_key)] = data
        else:
            # TODO: Implement exception handling
            print('ERROR')
    
    def load(self, key):
        if key in self.db:
            return self.db[key]
        else:
            # TODO: Implement exception handling
            print(f"***** {key} does not exists in the current database")
            return None

