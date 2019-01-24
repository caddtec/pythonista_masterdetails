import ui
import recerror


def ab_add_button_tapped(sender):
    raise recerror.MDNotImplementedError('The add_button hook in MDMasterListView ' +
                                             'has not been provided...')


def ab_edit_button_tapped(sender):
    raise recerror.MDNotImplementedError('The edit_button hook in MDMasterListView ' +
                                             'has not been provided...')


class MDTableViewDataSource (object):
    def __init__(self, data):
        self.data = data
    
    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.data)

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.text_label.text = self.data[row].title
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        # If this is not implemented, no section headers will be shown.
        return 'List of Items'

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return True

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return True

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        del self.data[row]
        self.data.clear()
        tableview.reload()

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        self.data.move(from_row, to_row)
    
    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        self.data.load(row)

    def tableview_did_deselect(self, tableview, section, row):
        # Called when a row was de-selected (in multiple selection mode).
        self.data.save(row)

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'

class MDMasterListView (ui.View):
    def __init__(self):
        self.table_view = None
        self.nav = None
    
    @property
    def list_view(self):
        return self.table_view
    
    @property
    def add_buttonitem(self):
        return self.list_view.right_button_items[0]
    
    @property
    def edit_buttonitem(self):
        return self.list_view.left_button_items[0]
    
    @property
    def list_title(self):
        return self.table_view.name
    
    @list_title.setter
    def list_title(self, value):
        self.table_view.name = value
    
    @property
    def view_title(self):
        return self.nav.name
    
    @view_title.setter
    def view_title(self, value):
        self.nav.name = value
    
    def prepare_view(self, ds=None, add_hook=ab_add_button_tapped,
                                    edit_hook=ab_edit_button_tapped):
        self.table_view = ui.TableView(flex='WHLRTB')
        self.table_view.allows_selection = True
        self.table_view.allows_multiple_selection = False
        self.table_view.right_button_items = ui.ButtonItem(image=ui.Image.named("typb:Plus"),
                                                           action=add_hook),
        self.table_view.left_button_items = ui.ButtonItem(image=ui.Image.named('typb:Edit'),
                                                          action=edit_hook),
        self.table_view.name = 'TV Name'
        
        if ds != None:
            self.table_view.data_source = self.table_view.delegate = ds
        
        self.nav = ui.NavigationView(self.table_view)
        self.nav.navigation_bar_hidden = False
        self.nav.frame = self.bounds
        self.nav.flex = "WH"
        self.nav.name = "Master List"
        self.add_subview(self.nav)

def main_sample():
    lst = ui.ListDataSource(['Item 1', 'Item 2', 'Item 3', 'Item 4'])
    table_view = ui.TableView(flex='WHLRTB')
    table_view.allows_selection = True
    table_view.allows_multiple_selection = False
    table_view.right_button_items = ui.ButtonItem(image=ui.Image.named("typb:Plus")),
    table_view.left_button_items = ui.ButtonItem(image=ui.Image.named('typb:Edit')),
    table_view.name = 'Table View Name'
    table_view.data_source = table_view.delegate = lst
    
    nav = ui.NavigationView(table_view)
    nav.navigation_bar_hidden = False
    nav.name = "Master List"
    nav.flex = "WHLRTB"
    nav.present('sheet')

def main_pyui():
    lst = ui.ListDataSource(['Pyui 1', 'Pyui 2', 'Pyui 3', 'Pyui 4'])
    v = ui.load_view('mastest')
    v.prepare_view(lst)
    v.present('sheet')

def main():
    lst = ui.ListDataSource(['Item 1', 'Item 2', 'Item 3', 'Item 4'])
    v = MDMasterListView(frame=(0,0,1000,500))
    v.prepare_view(lst)
    v.present('sheet')

if __name__ == '__main__':
    # main_sample()
    # main()
    main_pyui()

