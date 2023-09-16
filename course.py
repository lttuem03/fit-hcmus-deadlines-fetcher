from topic import Topic

class Course:
    name = ""
    url = ""

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.topics = [] # type: list[Topic]