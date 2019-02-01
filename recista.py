import recerror
import ui
import recmaster
import recdetail
import console
import yaml


def load_config(file_name):
    with open(file_name) as yfile:
        cfg = yaml.load(yfile)
    
    portal_view = ui.load_view(cfg['ui']['layout'])
    detail_views = {}
    for dviews in cfg['ui']['identifiers']['details']:
        dv = ui.load_view(dviews['pyui'])
        dv.name = dviews['title']
        dv_name = dviews['name']
        nav_flag = True
        if 'navigation' in dviews:
            nav_flag = bool(dviews['navigation'])
        portal_view[dv_name].prepare_view(dv, nav_flag)
        detail_views[dv_name] = dv
    
    return portal_view, detail_views, cfg


class MDDataSource (recmaster.MDTableViewDataSource):
    pass


class MDApp (object):
    def __init__(self, data, components=None):
        self.data = data
        self.detail = components
        self.check_components()
    
    @property
    def components(self):
        return self.detail
    
    def check_components(self):
        if self.components != None:
            if not 'master_list' in self.components:
                raise recerror.MDKeyError(msg='Key master_list not present in detail components')
    
    @components.setter
    def components(self, value):
        self.detail = value
        self.check_components()
    
    @property
    def master_view(self):
        try:
            return self.detail['master_list']
        except KeyError as kerr:
            raise recerror.MDKeyError(kerr, 'Unexpected error : Key master_list ' +
                                            'should exist as the master view.')
    
    @property
    def master_list(self):
        return self.master_view.list_view
    
    @property
    def edit_mode(self):
        return self.master_list.editing
    
    @edit_mode.setter
    def edit_mode(self, value):
        self.master_list.editing = value
    
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
    
    def append(self, id_key):
        raise recerror.MDNotImplementedError('The method append in parent class MDApp ' +
                                             'is abstract and should be implemented by the derived class...')
    
    def clear(self):
        for key in self.detail:
            if hasattr(self.detail[key], 'text'):
                self.detail[key].text = ''
    
    def load(self, key):
        raise recerror.MDNotImplementedError('The method load in parent class MDApp ' +
                                             'is abstract and should be implemented by the derived class...')
    
    def save(self, key):
        raise recerror.MDNotImplementedError('The method save in parent class MDApp ' +
                                             'is abstract and should be implemented by the derived class...')


class MDView (ui.View):
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
    
    # TODO Put every label as a parameterized setting with YAML
    def add_item_tapped(self, sender):
        self.data_app.append(console.input_alert('Add Item','Enter text for Item','My New Item','Submit'))
    
    def edit_items_tapped(self, sender):
        self.data_app.edit_mode = not self.data_app.edit_mode
    
    def prepare_view(self, config, app, view_name=None, cls_ds=MDDataSource):
        if view_name != None:
            self.name = view_name
        elif 'main_view.title' in config['labels']:
            self.name = config['labels']['main_view.title']
        
        self.data_app = app
        detail_items = config['ui']['detail_items']
        detail_dict = dict(master_list=self['master_list'])
        for item_dict in detail_items:
            for dv_name in item_dict:
                for component_name in item_dict[dv_name]:
                    detail_dict[component_name] = self[dv_name].detail_view[component_name]
        self.data_app.components = detail_dict
        
        m_view = self.data_app.master_view
        m_ds = cls_ds(self.data_app)
        
        list_title = None
        if 'master_list.title' in config['labels']:
            list_title = config['labels']['master_list.title']
        
        m_view.prepare_view(m_ds, list_title, self.add_item_tapped, self.edit_items_tapped)
        if 'master_list.header.title' in config['labels']:
            m_ds.header_title = config['labels']['master_list.header.title']
        if 'master_list.delete.label' in config['labels']:
            m_ds.del_btn_label = config['labels']['master_list.delete.label']
        
        pres = 'sheet'
        if 'present' in config['ui']:
            pres = config['ui']['present']
        self.present(pres)

