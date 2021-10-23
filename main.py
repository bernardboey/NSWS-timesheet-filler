import os

from nsws import TimesheetAdder, Timesheet

# For best practice, use environment variables for your username and password.
# For username, exclude "nusstu\". Should be of the form: "eXXXXXXX".
username = os.environ.get("NUSNET_1")  # Exclude "nusstu\". Should be of the form: "eXXXXXXX".
password = os.environ.get("NUSNET_PASSWORD_1")

# In a pinch, you can just type in your username and password directly here. Uncomment the 2 lines below.
# But do note that this is risky. PLEASE DO NOT COMMIT USERNAMES AND PASSWORDS INTO GITHUB.
# username = "ENTER USERNAME HERE"
# password = "ENTER PASSWORD HERE"

# Enter job url here (e.g. "https://inetapps.nus.edu.sg/nsws/app/student/jobs/view/hourly/JXXXXXXXXXX")
job_url = "Enter NSWS job url here"

# Fill in your timesheet data here. Dates must be dd/mm/yyyy. Timings must be hhmm (24 hr).
timesheet_data = [
    # Example:
    Timesheet(date='04/05/2021', time_in='1400', time_out='1600', break_='0000', gap='0000', others='0000', notes=''),
]

timesheet_adder = TimesheetAdder(username, password, job_url, timesheet_data)
