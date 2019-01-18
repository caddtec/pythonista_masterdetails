

class MDError (Exception):
    def __init__(self, msg):
        self.msg = msg


class MDNotImplementedError (MDError):
    pass


class MDNotDefinedError (MDError):
    pass

class MDKeyError (KeyError):
    def __init__(self, key_error = None, msg=''):
        self.msg = msg
        self.key_error = key_error

