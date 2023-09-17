import re
import unicodedata
import datetime as dt

def unicodeLen(unicode_string: str):
    """Return length of the unicode string 'as printed out'"""
    return len(unicodedata.normalize('NFC', unicode_string))

def get_due_datetime_from_str(due_str: str):
    """Interpret the due time string on Moodle into a datetime object / 
    Format: Monday, 13 March 2023, 9:40 AM
    (Note: 12:00 AM means 12:00 midday, 12:00 PM means 0:00 next day)"""

    # Set default values in case parsing gone wrong
    day = 1
    month = 1
    year = 1970
    hour = 0
    minute = 0

    # Extract the date values: day, month, year
    month_patterns = [r'January', r'February', r'March', r'April', r'May', r'June', r'July', r'August', r'September', r'October', r'November', r'December']

    for month_as_integer, month_as_str in enumerate(month_patterns, start=1):
        date_pattern = r'(\d+) (' + month_as_str + r') (\d+)'

        search_result = re.search(date_pattern, due_str)

        if search_result != None:
            day = int(search_result[1])
            month = month_as_integer
            year = int(search_result[3])

            break
    
    # Extract the time values, +1 day if needed (12 PM)
    if '12:00 PM' in due_str:
        hour = 0
        minute = 0
        return dt.datetime(day=day+1, month=month, year=year, hour=hour, minute=minute)
    
    time_pattern = r'(\d{1,2}):(\d{2}) (AM|PM)'

    search_result = re.search(time_pattern, due_str)

    hour = int(search_result[1])
    minute = int(search_result[2])

    if search_result[3] == 'PM':
        hour += 12
    
    return dt.datetime(day=day, month=month, year=year, hour=hour, minute=minute)