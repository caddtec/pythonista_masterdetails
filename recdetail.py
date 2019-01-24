import ui


class MDDetailView (ui.View):
    def __init__(self):
        self.detail_view = None
        self.nav = None
    
    def prepare_view(self, detail_view=None):
        self.detail_view = detail_view
        
        self.nav = ui.NavigationView(self.detail_view)
        self.nav.navigation_bar_hidden = False
        self.nav.frame = self.bounds
        self.nav.flex = "WH"
        self.nav.name = "Master Detail"
        self.add_subview(self.nav)

