from shelfdb import ShelfDB


# TODO: Put abstract DAO class with dao_model which throws exception
class FormDAO (object):
    @classmethod
    def dao_model(cls):
        print('*****ERROR****(TBC)')


class FormDB (ShelfDB):
    def save(self, pview):
        super().save({key: getattr(pview[key], self.model_info[key]) for key in self.model_info})
    
    def load(self, pview):
        loaded_values = super().load(getattr(pview[self.id_key], self.model_info[self.id_key]))
        if not isinstance(loaded_values, dict):
            loaded_values = loaded_values.__dict__
        for key in self.model_info:
            setattr(pview[key], self.model_info[key], loaded_values[key])
    
    @classmethod
    def create_form_db(cls, dao_type, form_name=None, form_key='recordID', values_storage=False):
        if not form_name:
            form_name = dao_type.__name__
        return cls(dao_type, prefix=form_name, id_key=form_key, is_rawdata=values_storage)

