import recista
import recmaster
import recdetail
import sample
import ui


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

class MyTableViewDataSource (recmaster.MDTableViewDataSource):
    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        # If this is not implemented, no section headers will be shown.
        return 'Master List NG'

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Erase NG'


class MyMasterView (recmaster.MDMasterListView):
    pass


class MyDetailView (recdetail.MDDetailView):
    pass


class MyView (recista.MDView):
    pass


v = ui.load_view()
dv = ui.load_view('sample_detail')
v['detail_view'].prepare_view(dv)
v.prepare_view(MyDataApp([sample.ItemDAO('Example', 'My Example Description')]),
               'Experimentation with Master-Details',
               MyTableViewDataSource,
               detail_items=['textview_detail'])

v.present('sheet')
