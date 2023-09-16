from assignment import Assignment

class Topic:
    name = ""
    
    def __init__(self, name):
        self.name = name
        self.assignments = [] # type: list[Assignment]