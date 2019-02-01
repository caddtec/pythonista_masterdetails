import recista
import sample


class MyDataApp (recista.MDApp):
    @property
    def description(self):
        return self.components['textview_detail'].text
    
    @description.setter
    def description(self, key):
        self.components['textview_detail'].text = self[key].description
    
    def append(self, id_key):
        self.data.append(sample.ItemDAO(id_key, 'Place description here...'))
        self.master_list.reload()
        self.master_list.selected_row = self.description = len(self.data) - 1
    
    def load(self, key):
        self.description = key
    
    def save(self, key):
        self[key].description = self.description


v, _, cfg = recista.load_config('md_config.yaml')

# To be deleted... only for debugging
import pprint
pprint.pprint(cfg, width=1)

v.prepare_view(cfg, MyDataApp([sample.ItemDAO('Example', 'My Example Description')]))
