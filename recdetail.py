import ui


class MDDetailView (ui.View):
    def __init__(self):
        self.detail_view = {}
        self.nav = None
    
    def prepare_view(self, detail_view=None, navigation=True):
        self.detail_view[detail_view.unique_id] = detail_view
        
        if navigation:
            self.nav = ui.NavigationView(detail_view)
            self.nav.navigation_bar_hidden = False
            self.nav.frame = self.bounds
            self.nav.flex = "WH"
            self.nav.name = "Master Detail"
            self.add_subview(self.nav)
        else:
            detail_view.frame = self.bounds
            detail_view.flex = "WH"
            self.add_subview(detail_view)

class MDDetailViewWidget (ui.View):
    def __init__(self):
        self.unique_id = None

