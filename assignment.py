import re
import datetime as dt
import unicodedata

from utils import unicodeLen, get_due_datetime_from_str

class Assignment:
    name = ""
    url = ""
    course = ""

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.due = dt.datetime.now()
        self.submission_status = False

    def __str__(self):
        return "{} - {} - Due: {} - Submitted: {}".format(self.name, self.course, self.due.strftime("%A, %d/%m/%Y,  %H:%M"), self.submission_status)
    
    def setCourse(self, course):
        self.course = course

class AssignmentTable:
    buffer = ""

    def __init__(self, assignment_list: list[Assignment]):
        self.assignment_list = assignment_list
        self.craftTable()

    def craftTable(self, fields: list[(str, int)] = [("Assignment", 32), ("Course", 24), ("Due", 30), ("Submitted", 9)], border_width = 2):
        header = ""
        seperator = ""

        for field_name, field_len in fields:
            header += "{:<{len}}".format(field_name, len=field_len + border_width)
            seperator += "{"":{fill}>{width}}".format(" " * border_width, fill= '=', width=field_len + border_width)
        
        header += "\n"
        seperator += "\n"

        self.buffer += "\n" + header + seperator

        if len(self.assignment_list) == 0:
            self.buffer += "\n"
            self.buffer += seperator
            return

        assignment_list_sorted = sorted(self.assignment_list, key=lambda assignment:assignment.due)

        name_field_len = fields[0][1]
        course_field_len = fields[1][1]
        due_field_len = fields[2][1]
        submitted_field_len = fields[3][1]

        for assignment in assignment_list_sorted:
            # Assignment name
            if unicodeLen(assignment.name) <= name_field_len:
                name_field = unicodedata.normalize('NFC', assignment.name)
            else:
                name_field = unicodedata.normalize('NFC', assignment.name)[:name_field_len - 3] + "..."

            # Assignment course
            if unicodeLen(assignment.course) <= course_field_len:
                course_field = unicodedata.normalize('NFC', assignment.course)
            else:
                course_field = unicodedata.normalize('NFC', assignment.course)[:course_field_len - 3] + "..."

            # Due date
            day_of_week_part =  assignment.due.strftime("(%A)")
            date_part = assignment.due.strftime("%d/%m/%Y")
            time_part = assignment.due.strftime("%H:%M")
            due_field = "{time:<5}, {date:<10} {day_of_week:<12}".format(day_of_week=day_of_week_part, date=date_part, time=time_part)
            
            if len(due_field) > due_field_len:
                due_field = due_field[:due_field_len - 3] + "..."
            
            # Submitted
            if assignment.submission_status:
                submitted_field = "[x]"
            else:
                submitted_field = "[ ]"

            self.buffer += "{name:<{name_len}}{border}{course:<{course_len}}{border}{due:<{due_len}}{border}{submitted:^{submitted_len}}\n".format(border=" " * border_width, name=name_field, name_len=name_field_len, course=course_field, course_len=course_field_len, due=due_field, due_len=due_field_len, submitted=submitted_field, submitted_len=submitted_field_len)

        self.buffer += seperator

    def print(self):
        print(self.buffer)