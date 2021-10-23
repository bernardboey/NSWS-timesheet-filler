import dataclasses
import datetime
import collections

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select


Timesheet = collections.namedtuple("Timesheet", ["date", "time_in", "time_out", "break_", "gap", "others", "notes"])


@dataclasses.dataclass
class TimesheetEntry:
    # All timings must be double digit 24-hour
    # E.g. "00" or "09" or "19"
    time_in_hour: str
    time_in_min: str
    time_out_hour: str
    time_out_min: str
    break_time_hour: str
    break_time_min: str
    gap_hour_hour: str
    gap_hour_min: str
    others_hour: str
    others_min: str

    student_notes: str

    year: str  # 4 digit year
    month: str  # Full spelling
    day: str  # Single digit if less than 10 (e.g. "6" or "16")

    raw_date: str

    @classmethod
    def parse(cls, timesheet: Timesheet):
        datetime_obj = datetime.datetime.strptime(timesheet.date, "%d/%m/%Y")
        return cls(time_in_hour=timesheet.time_in[:2], time_in_min=timesheet.time_in[2:],
                   time_out_hour=timesheet.time_out[:2], time_out_min=timesheet.time_out[2:],
                   break_time_hour=timesheet.break_[:2], break_time_min=timesheet.break_[2:],
                   gap_hour_hour=timesheet.gap[:2], gap_hour_min=timesheet.gap[2:],
                   others_hour=timesheet.others[:2], others_min=timesheet.others[2:],
                   student_notes=timesheet.notes,
                   year=str(datetime_obj.year), month=datetime_obj.strftime("%B"), day=str(datetime_obj.day),
                   raw_date=timesheet.date)


class TimesheetAdder:
    def __init__(self, username: str, password: str, job_url: str, data):
        self.username = username
        self.password = password
        self.job_url = job_url
        timesheet_entries = [TimesheetEntry.parse(timesheet) for timesheet in data]

        self.driver = self.setup_driver()
        self.login()
        self.remove_duplicate_entries(timesheet_entries)
        for entry in timesheet_entries:
            self.add_timesheet(entry)

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def login(self):
        self.driver.get(self.job_url)

        # Click on login button
        self.wait_to_click(By.XPATH, "//form/div/button")

        # Input username and password
        self.input(f"nusstu\\{self.username}", By.ID, "userNameInput")
        self.input(self.password, By.ID, "passwordInput")

        # Click on submit button
        self.click(By.ID, "submitButton")

        # We make sure to wait for page to load, otherwise we would not have fully logged in.
        self.wait(By.XPATH, "//app-student-menu/nav/div/div[1]/ul/li[4]")
        self.driver.get(self.job_url)

    def wait(self, by: str, value: str):
        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.1)
        return wait.until(expected_conditions.element_to_be_clickable((by, value)))

    def wait_to_click(self, by: str, value: str):
        self.wait(by, value).click()

    def input(self, text: str, by: str, value: str):
        element = self.driver.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def click(self, by: str, value: str):
        self.driver.find_element(by, value).click()

    def add_timesheet(self, entry: TimesheetEntry):
        # Click on "add new timesheet" button. We make sure to wait for job timesheet page to load.
        self.wait_to_click(By.XPATH, "//app-student-timesheet-hourly/div/div/div/button")

        self.input(entry.time_in_hour, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[1]/div[2]/div/app-nsws-timepicker/table/tr[2]/td[1]/input")
        self.input(entry.time_in_min, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[1]/div[2]/div/app-nsws-timepicker/table/tr[2]/td[3]/input")

        self.input(entry.time_out_hour, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[1]/div[3]/div/app-nsws-timepicker/table/tr[2]/td[1]/input")
        self.input(entry.time_out_min, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[1]/div[3]/div/app-nsws-timepicker/table/tr[2]/td[3]/input")

        self.input(entry.break_time_hour, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[1]/div[4]/div/app-nsws-timepicker/table/tr[2]/td[1]/input")
        self.input(entry.break_time_min, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[1]/div[4]/div/app-nsws-timepicker/table/tr[2]/td[3]/input")

        self.input(entry.gap_hour_hour, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[2]/div[2]/div/app-nsws-timepicker/table/tr[2]/td[1]/input")
        self.input(entry.gap_hour_min, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[2]/div[2]/div/app-nsws-timepicker/table/tr[2]/td[3]/input")

        self.input(entry.others_hour, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[2]/div[3]/div/app-nsws-timepicker/table/tr[2]/td[1]/input")
        self.input(entry.others_min, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[2]/div[3]/div/app-nsws-timepicker/table/tr[2]/td[3]/input")

        self.input(entry.student_notes, By.XPATH,
                   "//app-student-timesheet-form/div/form"
                   "/div[2]/div[3]/div[3]/div/textarea")

        # Click on date picker
        self.click(By.XPATH, "//app-student-timesheet-form/div/form/div[1]/div[1]/div[1]/div/input")

        # Click on dear picker
        self.click(By.XPATH, "//bs-datepicker-navigation-view/button[3]")

        # Select year
        self.click(By.XPATH, f"//bs-calendar-layout//*[text()='{entry.year}']")

        # Select month
        self.click(By.XPATH, f"//bs-calendar-layout//*[text()='{entry.month}']")

        # Select date
        self.click(By.XPATH, f"//bs-calendar-layout//td[@role='gridcell']"
                             f"//*[text()='{entry.day}' and not(contains(@class, 'is-other-month'))]")

        # Click on "save as draft" button
        self.click(By.XPATH, "//app-student-timesheet-form/div/form/div[3]/button[1]")

    def get_all_timesheet_rows(self):
        # Wait for add new button to make sure that the page has loaded
        self.wait(By.XPATH, "//app-student-timesheet-hourly/div/div/div/button")

        # Select all items to be displayed
        select = Select(self.wait(By.XPATH, "//app-nsws-data-table-v2/div[2]/div/div/select"))
        select.select_by_visible_text("All")
        return self.driver.find_elements(By.XPATH, "//app-nsws-data-table-v2/div/table/tbody/tr")

    def delete_all_draft_timesheets(self):
        while True:
            for row in self.get_all_timesheet_rows():
                elements = row.find_elements(By.TAG_NAME, "td")
                buttons = elements[-1].find_elements(By.TAG_NAME, "button")
                if buttons:
                    e_delete_button = buttons[1]
                    e_delete_button.click()
                    self.click(By.XPATH, "//app-student-timesheet-hourly/div/div/div/div/button[1]")
                    break
            else:
                break

    def remove_duplicate_entries(self, entries: list[TimesheetEntry]):
        for row in self.get_all_timesheet_rows():
            elements = row.find_elements(By.TAG_NAME, "td")
            date_string = elements[1].text
            time_in_string = elements[2].text
            time_out_string = elements[3].text

            date = date_string[-10:]
            time_in_hour = time_in_string[:2]
            time_in_min = time_in_string[-2:]
            time_out_hour = time_out_string[:2]
            time_out_min = time_out_string[-2:]
            for entry in entries.copy():
                if (entry.raw_date == date and entry.time_in_hour == time_in_hour and entry.time_in_min == time_in_min
                        and entry.time_out_hour == time_out_hour and entry.time_out_min == time_out_min):
                    entries.remove(entry)
