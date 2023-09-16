# fit-hcmus-deadlines-fetcher

## Description
A small tool that help me and potentially other students at FIT@HCMUS track their unsubmitted assignments on my university's Moodle. 

## Why would I need this ?
Normally, I need to go on the Moodle, login, click the link of whatever courses I'm enrolled in, click the assignment link, all that just to know when the assignment is due. I find that's too much work, and I can possibly missout on new assignments too. So I built this to collect info of all the assignments I need to work on, their due dates and submission statuses, all neatly packed in a table.

## Target user
This tool is very niched as it only works with FIT@HCMUS' Moodle system. But the way the scripts work might potentially be feasible for your courses system as well, so feel free to fork and edit it to suit your own needs!

## Prerequisites
This tool utilize the [twill](https://github.com/twill-tools/twill "twill: a simple scripting language for web browsing")'s Python API to access Moodle directly in code.
Make sure you install twill before running the scripts by typing the following into any command line tool (cmd, Shell, Git Bash, etc.):
```
pip install twill
```
**IMPORTANT**: To be able to login to FIT@HCMUS Moodle from this tool, you need to disable the Microsoft 365 login method if your account was **exclusively** using Microsoft 365 to login. To do this, go to Moodle's main page, on the right there's this panel called 'Microsoft', there're options and instructions on how to do this. You just need to be able to login using your Student ID and a password.

## Using this tool
You can fork/download the python scripts here, then just run the `fetch.py` file, login using your username and password, wait a bit for the program to fetch your courses info from Moodle, then edit the `active_course_list.txt` file (if it was your first time running, or the file isn't already there, then it will be created for you) to choose which courses/topic sections you're currently following. `fetch.py` will based on the `active_course_list.txt` to show you only what you need. \
\
**NOTE**: If it is your first time running, or there was some changes on the courses' topic list on Moodle (you might need to delete the `active_course_list.txt` file in this case so it can be renewed), you will need to run `fetch.py` twice, the first time to create/renew the `active_course_list.txt`, the second time to show you your assignments info. 
