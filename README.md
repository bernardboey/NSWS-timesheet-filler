# NSWS Timesheet Filler
A script to automatically fill your timesheets on [NSWS (NUS Student Work Scheme)](https://inetapps.nus.edu.sg/nsws/app/login).

## Installation and Setup

#### 1. Python

Use Python 3.9 or 3.10. To install the required Python dependencies (Selenium), run the following command:
`pip install -r requirements.txt`

#### 2. Selenium

Selenium requires a webdriver. For this project, we are using the Chrome webdriver.
First, you need to make sure you have Chrome installed.
Then, you need to download/install the **correct version** of the Chrome webdriver that corresponds to your version of Chrome.

For windows, you can download and extract the `chromedriver.exe` file [here](https://sites.google.com/chromium.org/driver/).
Then, you can either put the file in the root folder of this repository (short-term solution),
or you can include the location of the file in your PATH environment variable (long-term solution that allows you to use it for other projects).

For mac, the easiest way is to install via Homebrew: `brew install chromedriver`.
Alternatively, you can download and extract the `chromedriver` file [here](https://sites.google.com/chromium.org/driver/).
Then, you can either put the file in the root folder of this repository (short-term solution),
or you can include the location of the file in your PATH environment variable (long-term solution that allows you to use it for other projects).

## Usage

*By using this script, you acknowledge that you are responsible for any potential errors and consequences, including but not limited to:
Errors in timesheet information and the risks of browser automation.
The creator(s) and maintainer(s) of this script cannot be held liable for any such errors and consequences.*

1. Open `main.py`
2. Enter your NUSNET username and password. For username, exclude "nusstu\". It should be of the form: `eXXXXXXX`.
   1. Option 1 is to store them as environment variables. This is generally safer than the other option.
   2. Option 2 is to just type it in the file. Note that this is risky. *DO NOT commit usernames and passwords into GitHub*
3. Enter the NSWS job url for the job that you want to submit timesheets for (e.g. "https://inetapps.nus.edu.sg/nsws/app/student/jobs/view/hourly/JXXXXXXXXXX").
This should be the link that displays your existing timesheets.
4. Fill in your timesheet data according to the specified format. Dates must be dd/mm/yyyy. Timings must be hhmm (24 hr).
```python
timesheet_data = [
    Timesheet(date='04/05/2021', time_in='1400', time_out='1600', break_='0000', gap='0000', others='0000', notes=''),
    Timesheet(date='05/05/2021', time_in='1500', time_out='1700', break_='0000', gap='0000', others='0000', notes=''),
    ...
]
```
5. Run `main.py`. You can do this via your IDE or via the command line (`python main.py`).
6. Upon executing the file, a browser should pop up, and the timesheets will be added automatically.
7. Once completed, the browser will remain open, and you can review that the information has been keyed in correctly.
8. If correct, select the timesheets that were added and click on the submit button. (Alternatively, you can keep them as drafts and submit them another time)
9. Once done, you can close the browser.

Note that this script **DOES NOT submit the timesheet for approval**.
You will need to click on the submit button yourself, otherwise the timesheets will remain as drafts and will not be submitted.
When you do that, please also take the time to **verify that all the information has been keyed in correctly**.
Be careful to submit ALL timesheets that you have added, as timesheets on a different page will not be selected automatically.
To be safe, you can select the "All" option to show all items (at the bottom left of the page).

## Troubleshooting

If you encounter any technical issues, please contact Bernard on Telegram ([@bernard_boey](https://t.me/bernard_boey)).

If for some reason you need to delete all the (draft) timesheets that you have added,
you can do the following in the `main.py` file:
```
timesheet_adder.delete_all_draft_timesheets()
```

Note that you cannot delete timesheets that have already been submitted for approval.