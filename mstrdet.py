import ui
import console


class ItemDAO (object):
    def __init__(self, title, description):
        self._title = title
        self._description = description
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = value
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value


class MyDataApp (object):
    def __init__(self, data, components):
        self.data = data
        self.detail = components
    
    @property
    def description(self):
        return self.detail['description_textview'].text
    
    @description.setter
    def description(self, key):
        self.detail['description_textview'].text = self[key].description
    
    @property
    def edit_mode(self):
        return self.detail['master_tv'].editing
    
    @edit_mode.setter
    def edit_mode(self, value):
        self.detail['master_tv'].editing = value
    
    def __getitem__(self, name):
        return self.data[name]
    
    def __setitem__(self, name, value):
        self.data[name] = value
    
    def __len__(self):
        return len(self.data)
    
    def __delitem__(self, key):
        del self.data[key]
    
    def move(self, from_row, to_row):
        imov = self.data.pop(from_row)
        self.data.insert(to_row, imov)
    
    def append(self, title):
        self.data.append(ItemDAO(title, 'Place description here...'))
        self.detail['master_tv'].reload()
        self.detail['master_tv'].selected_row = self.description = len(self.data) - 1
    
    def clear(self):
        self.detail['description_textview'].text = ''
    
    def load(self, key):
        self.description = key
    
    def save(self, key):
        self[key].description = self.description


class MyTableViewDataSource (object):
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
        return 'Master Data'

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


class MyView (ui.View):
    def __init__(self):
        # This will also be called without arguments when the view is loaded from a UI file.
        # You don't have to call super. Note that this is called *before* the attributes
        # defined in the UI file are set. Implement `did_load` to customize a view after
        # it's been fully loaded from a UI file.
        pass
    
    @property
    def data_app(self):
        return self._dbdata
    
    @data_app.setter
    def data_app(self, value):
        self._dbdata = value

    def did_load(self):
        # This will be called when a view has been fully loaded from a UI file.
        pass

    def will_close(self):
        # This will be called when a presented view is about to be dismissed.
        # You might want to save data here.
        pass

    def draw(self):
        # This will be called whenever the view's content needs to be drawn.
        # You can use any of the ui module's drawing functions here to render
        # content into the view's visible rectangle.
        # Do not call this method directly, instead, if you need your view
        # to redraw its content, call set_needs_display().
        # Example:
        pass

    def layout(self):
        # This will be called when a view is resized. You should typically set the
        # frames of the view's subviews here, if your layout requirements cannot
        # be fulfilled with the standard auto-resizing (flex) attribute.
        pass

    def touch_began(self, touch):
        # Called when a touch begins.
        pass

    def touch_moved(self, touch):
        # Called when a touch moves.
        pass

    def touch_ended(self, touch):
        # Called when a touch ends.
        pass

    def keyboard_frame_will_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass

    def keyboard_frame_did_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass
    
    def add_item_tapped(self, sender):
        self.data_app.append(console.input_alert('Add Item','Enter text for Item','My New Item','Submit'))
    
    def edit_items_tapped(self, sender):
        self.data_app.edit_mode = not self.data_app.edit_mode


v = ui.load_view()
v.name = 'Experimentation with Master-Details'
v.data_app = MyDataApp([ItemDAO('Example', 'My Example Description')],
                       dict(description_textview=v['textview_detail'],
                            master_tv=v['tableview_master']))

v['tableview_master'].data_source = v['tableview_master'].delegate = MyTableViewDataSource(v.data_app)

v['button_additem'].action = v.add_item_tapped
v['button_edit'].action = v.edit_items_tapped

v.present('sheet')
