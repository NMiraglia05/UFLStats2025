from SeasonGenerator import SeasonStats
from Weeks import week
from WeekGenerator import WeeklyStats
from dashboardupdate import UpdateDashboard
import os
import shutil

weeknumber=week() # gets the week number. Note that this code is typically run on Sunday evening- if you run this code the day after, it will not be for the previous week.
SeasonStats() # this updates the seasonstats page
weeknumber=weeknumber-1
WeeklyStats(weeknumber) # this creates an excel file for that week's stats
UpdateDashboard()
if not os.path.exists(f'C:\\Users\\miragn\\Python\\UFL\\SeasonStats\\Week{weeknumber}.xlsx'):
    shutil.copy("C:\\Users\\miragn\\Python\\UFL\\SeasonStats.xlsx",f'C:\\Users\\miragn\\Python\\UFL\\SeasonStats\\Week{weeknumber}.xlsx') # this duplicates the seasonstats file for a particular week for archival purposes
else:
    pass
print('Done!')
