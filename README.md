# fit-hcmus-deadlines-fetcher

## Table of contents
- [Description](https://github.com/lttuem03/fit-hcmus-deadlines-fetcher#description)
- [Why would I need this ?](https://github.com/lttuem03/fit-hcmus-deadlines-fetcher#why-would-i-need-this-)
- [Target user](https://github.com/lttuem03/fit-hcmus-deadlines-fetcher#target-user)
- [Prerequisites](https://github.com/lttuem03/fit-hcmus-deadlines-fetcher#prerequisites)
- [Using this tool](https://github.com/lttuem03/fit-hcmus-deadlines-fetcher#using-this-tool)
- [How the script works](https://github.com/lttuem03/fit-hcmus-deadlines-fetcher#how-the-script-works)

## Description
A small tool that help me and potentially other students at FIT@HCMUS track their unsubmitted assignments on my university's Moodle. 

## Why would I need this ?
Normally, I need to go on the Moodle, login, click the link of whatever courses I'm enrolled in, click the assignment link, all that just to know when the assignment is due. I find that's too much work, and I can possibly missout on new assignments too. So I built this to collect info of all the assignments I need to work on, their due dates and submission statuses, all neatly packed in a table. For example:
```
Assignment                        Course                    Due                             Submitted  
================================  ========================  ==============================  =========  
Sample assignment #1              Sample course #1          14:30, 04/03/2023 (Saturday)       [ ]     
Sample assignment #2              Sample course #2          08:10, 08/04/2023 (Saturday)       [x]     
Sample test #1                    Sample course #3          09:10, 09/05/2023 (Tuesday)        [x]     
Sample test #2                    Sample course #4          08:15, 13/05/2023 (Saturday)       [ ]     
================================  ========================  ==============================  =========
```

## Target user
This tool is very niched as it only works with FIT@HCMUS' Moodle system. But the way the scripts work might potentially be feasible for your courses system as well, so feel free to fork and edit it to suit your own needs!

## Prerequisites
This tool utilize the [twill](https://github.com/twill-tools/twill "twill: a simple scripting language for web browsing")'s Python API to access Moodle directly in code.
Make sure you install twill before running the scripts by typing the following into any commandline-based tool (cmd, PowerShell, Git Bash, etc.):
```
pip install twill
```
**IMPORTANT**: To be able to login to FIT@HCMUS Moodle from this tool, you need to disable the Microsoft 365 login method if your account was **exclusively** using Microsoft 365 to login. To do this, go to Moodle's main page, on the right there's this panel called 'Microsoft', there're options and instructions on how to do this. You just need to be able to login using your Student ID and a password.

## Using this tool
You can fork/download the python scripts here, then just run the `fetch.py` file in any commandline-based tool:
```
..\fit-hcmus-deadlines-fetcher> python fetch.py [-u=yourusername] [-p=yourpassword]
```
\
(__You can skip the typing in the login part by using BOTH the "-u" and "-p" in your command, this can help a lot if you're using bat file to run the scripts, as shown below.__) \
\
**HINT**: Here's how to make a psuedo executable on Windows by using Batch scripting: create a file ending in .bat, edit its contents with following 3 commands:
```
cd "<the directory in which the python scripts are>"
python fetch.py -p=myusername -u=mypassword
pause
:: Note that if the scripts are on another disk (eg. D:\) you must prefix the directory with /<name of the this>. For example:
:: cd /d "D:\fit-hcmus-deadlines-fetcher"
```
## How the script works
The general idea is, fetching all the assignment's page html from the web using [twill](https://github.com/twill-tools/twill "twill: a simple scripting language for web browsing")'s virtual browser, then use regexes to find all the information needed (urls, course names, assignment names, etc.), save them all into objects, finally create a table based on those objects and print it out. \
\
In details, the fetching flow goes like this: Fetch the login page > Login > Fetch the assignments from the 'Calendar/Upcoming Events' tab > For each assignment, fetch the due date and submission info. \
\
This idea can be applied to any Moodle-based course-management systems, so feel free to create your own version!

