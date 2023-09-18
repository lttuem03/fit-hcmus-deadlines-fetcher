import os.path
import re
import sys

from twill import browser
from twill.commands import formclear, fv, submit

from course import Course
from topic import Topic
from assignment import Assignment, AssignmentTable

from utils import get_due_datetime_from_str

moodle_host = 'courses.fit.hcmus.edu.vn'
moodle_https = 'https://' + moodle_host

def fetch_argv_login_info():
    if len(sys.argv) < 3:
        return "", ""
    
    argv_username = ""
    argv_password = ""

    username_arg_pattern = r'-u=(\w+)'
    password_arg_pattern = r'-p=([\w\.]+)'

    for argv in sys.argv:
        match_username = re.match(username_arg_pattern, argv)
        if match_username != None:
            argv_username = match_username[1]
            continue
        match_password = re.match(password_arg_pattern, argv)
        if match_password != None:
            argv_password = match_password[1]
    
    return argv_username, argv_password

def login(argv_username = "", argv_password = ""):
    print("Log into FIT@HCMUS Moodle:")
    
    if argv_username == "" or argv_password == "":
        username = input("Username: ")
        password = input("Password: ")
    else:
        username = argv_username
        password = argv_password
        print("Username: " + username)
        print("Password: " + password)

    login_failed_id = 'loginerrormessage'

    print("\nLogging in...")
    
    # Go to FIT moodle, redirecting to login page
    browser.go(moodle_https)

    # Fill in the fields
    formclear(1)
    fv(1, 'username', username)
    fv(1, 'password', password)

    # Click Login button
    submit('loginbtn')

    if browser.html.find(login_failed_id) == -1:
        # Login successful
        print("\nLogged in")
        return True
    
    # Login failed
    print("\nFailed to log in")
    return False

def fetch_courses():
    """Fetch the courses' name and URL from the main page html"""

    print("\nFetching courses...")
    courses = []
    main_page_html = browser.html

    course_ids = re.findall(r'data-courseid="(\d+)"', main_page_html)
    course_ids = [Id for Id in course_ids if Id != '1'] # Filter out '1'

    base_course_url = 'https://courses.fit.hcmus.edu.vn/course/view.php?id='
    base_course_pattern = r'https:\/\/courses\.fit\.hcmus\.edu\.vn\/course\/view\.php\?id='

    for cid in course_ids:
        course_url = base_course_url + cid
        course_pattern = base_course_pattern + cid

        match = re.search(course_pattern, main_page_html)

        if match != None:
            span = match.span()
            start = main_page_html[span[1]:].find('>') + span[1]
            end = main_page_html[span[1]:].find('<') + span[1]

            course_name = main_page_html[start+1:end]
            courses.append(Course(course_name, course_url))
    
    return courses

def fetch_topics_and_assignments(courses: list[Course]):
    """Go through each course and extract their topics and assignments by chipping away at the html lol"""
    for course in courses:
        browser.go(course.url)
        course_content = browser.html

        # Extract only after the main region (containing the topics and assignment) from the course html
        region_main_section_beginning = r'<section id="region-main"'

        region_main_section_beginning_search = re.search(region_main_section_beginning, course_content)
        if region_main_section_beginning_search == None:
            continue
        
        span = region_main_section_beginning_search.span()
        course_content = course_content[span[0]:]

        # Extract the topic (in the html, they are called sections)
        section_beginning = r'<li id="section-\d+"'
        section_beginning_search = re.findall(section_beginning, course_content)

        sectionname_beginning = r'<h3 id="sectionid-(\d+)-title" class="sectionname'
        activity_assign_beginning = r'<li class="activity assign modtype_assign'
        aalink_beginning = r'<a class="aalink"'
        instancename_beginning = r'<span class="instancename">'

        for section_id, section in enumerate(section_beginning_search):
            if section_id + 1 < len(section_beginning_search):
                this_section_start = re.search(section, course_content).span()[0]
                this_section_end = re.search(section_beginning_search[section_id + 1], course_content).span()[0]

                section_contents = course_content[this_section_start:this_section_end]
            else:
                section_contents = course_content[this_section_end:]

            # Extract section name
            find_sectionname_match = re.search(sectionname_beginning, section_contents)
            trim_from_here = find_sectionname_match.span()[0]
            section_contents = section_contents[trim_from_here:]
            sectionname_span_beginning = section_contents.find('<span>')
            sectionname_span_ending = section_contents.find('</span>')
            topic_name = section_contents[sectionname_span_beginning + 6:sectionname_span_ending].replace('&amp;', '&')
            
            new_topic = Topic(topic_name)
            
            # Extract the assignments in the topic
            activity_assign_beginning_search = re.search(activity_assign_beginning, section_contents)
            while activity_assign_beginning_search != None:
                trim_from_here = activity_assign_beginning_search.span()[0]
                section_contents = section_contents[trim_from_here:]
                # Extract assignment URL
                aalink_beginning_search = re.search(aalink_beginning, section_contents)
                trim_from_here = aalink_beginning_search.span()[0]
                section_contents = section_contents[trim_from_here:]
                href_begining = section_contents.find('href="')
                href_ending = section_contents.find('">')
                assignment_url = section_contents[href_begining + 6: href_ending]
                # Extract assignment name
                instancename_beginning_search = re.search(instancename_beginning, section_contents)
                trim_from_here = instancename_beginning_search.span()[1]
                section_contents = section_contents[trim_from_here:]
                instancename_ending = section_contents.find('<')
                assignment_name = section_contents[:instancename_ending].replace('&amp;', '&')
                new_topic.assignments.append(Assignment(assignment_name, assignment_url))
                section_contents = section_contents[instancename_ending:]
                activity_assign_beginning_search = re.search(activity_assign_beginning, section_contents)

            course.topics.append(new_topic)

    print("\nCOMPLETE")

def create_active_course_list(courses: list[Course]):
    with open('active_course_list.txt', 'w') as writer:
        for course in courses:
            writer.write("[ ] COURSE: " + course.name + "\n")
            
            for topic in course.topics:
                if topic.name != 'General':
                    writer.write("    [x] TOPIC: " + topic.name + "\n")
                else:
                    writer.write("    [ ] TOPIC: " + topic.name + "\n")
    
    print("Active course list created, edit the file and check [x] every course and topic you need to follow")

def filter_unactive_courses(courses: list[Course]):
    active_courses = []
    active_course_pattern = r'\[x\] COURSE: (.+)'

    with open('active_course_list.txt', 'r') as reader:
        file_contents = reader.read()
        active_courses_name = re.findall(active_course_pattern, file_contents)

        for course in courses:
            if course.name in active_courses_name:
                # Filter out the topics before appending to active course list
                search_course_in_file_content = re.search(course.name, file_contents)
                trim_from_here = search_course_in_file_content.span()[0]
                course_contents = file_contents[trim_from_here:] 
                course_contents_in_lines = course_contents.splitlines()

                active_topic_names = [] # store names of the active topics of this active course

                for line in course_contents_in_lines:
                    if re.match(r'\[[x ]\] COURSE: (.+)', line) != None: # iterate til the next '[ ] COURSE:' line
                        break

                    match_active_topic = re.match(r'    \[x\] TOPIC: (.+)', line)
                    
                    if match_active_topic != None:
                        active_topic_names.append(match_active_topic[1])

                course.topics = [topic for topic in course.topics if topic.name in active_topic_names]

                active_courses.append(course)
    
    return active_courses

def fetch_assignments(courses: list[Course]):
    print("\nFetching assignments...")
    due_date_beginning = r'<strong>Due:</strong> '
    submission_status_find = r'Submission status'
    submitted_status_find = r'Submitted for grading'
    unsubmitted_status_find = r'No attempt'
    
    assignment_list = []

    for course in courses:
        for topic in course.topics:
            for assignment in topic.assignments:
                browser.go(assignment.url)

                page_contents = browser.html

                # Set course
                assignment.setCourse(course.name)

                # Extract due dates
                due_date_beginning_search = re.search(due_date_beginning, page_contents)

                if due_date_beginning_search == None:
                    continue
                
                trim_from_here = due_date_beginning_search.span()[1]
                page_contents = page_contents[trim_from_here:]

                due_date_ending_search = page_contents.find('</div>')

                due_str = page_contents[:due_date_ending_search-13]
                assignment.due = get_due_datetime_from_str(due_str)

                # Extract submission info
                submission_status_find_search = re.search(submission_status_find, page_contents)
                trim_from_here = submission_status_find_search.span()[0]
                page_contents = page_contents[trim_from_here:]

                if re.search(submitted_status_find, page_contents) != None:
                    assignment.submission_status = True

                assignment_list.append(assignment)

    print("\nCOMPLETE")
    return assignment_list

def printStuffs(courses: list[Course]):
    for course in courses:
        print("\nCOURSE NAME: " + course.name)
        print("COURSE URL: " + course.url)
        print("COURSE CONTENTS:")

        for topic in course.topics:
            print("TOPIC: " + topic.name)

            for assignment in topic.assignments:
                print(assignment) 

if __name__ == "__main__":
    
    argv_username, argv_password = fetch_argv_login_info()

    if login(argv_username, argv_password) == False:
        sys.exit(1)

    courses = fetch_courses()
    fetch_topics_and_assignments(courses)

    if os.path.exists('active_course_list.txt') == False:
        create_active_course_list(courses)
    
    courses = filter_unactive_courses(courses)
    assignments = fetch_assignments(courses)
    
    table = AssignmentTable(assignment_list=assignments)
    
    if "-a" in sys.argv or "--all" in sys.argv:
        table.craftTable(include_submitted=True)
    else:
        table.craftTable(include_submitted=False)

    os.system('cls')
    print("Here are the assignments for your active courses:")
    table.print()

    sys.exit(0)