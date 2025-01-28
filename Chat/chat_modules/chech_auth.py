class ChechAuth:
    def __init__(self):
        self.key = "test"
        self.session = ""
        self.user = None
    
    def __call__(self, **kwds):
        
        """"
        check if the user is authenticated and provide the right api key
        """
        user = kwds.get("user")
        session = kwds.get("session")
        key = kwds.get("key")
        if key == self.key and (session != self.session or session is not None) and user is not None:
            return True
        return False