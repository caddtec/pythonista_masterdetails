

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
