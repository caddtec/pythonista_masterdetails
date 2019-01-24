

class ItemDAO (object):
    def __init__(self, title, description):
        self.title = title
        self.description = description
    
    @classmethod
    def dao_model(cls):
        return cls('text', 'text').__dict__

