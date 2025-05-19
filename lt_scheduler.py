import re
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from playwright.sync_api import Playwright, sync_playwright
import time

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

def get_next_tuesday_label():
    today = datetime.today()
    days_until_next_tuesday = (1 - today.weekday() + 7) % 7
    if days_until_next_tuesday == 0:
        days_until_next_tuesday = 7  # It's Tuesday today → go to next Tuesday
    next_tuesday = today + timedelta(days=days_until_next_tuesday)
    return next_tuesday.strftime("Tuesday %-m/%-d")  # Unix/Mac

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://my.lifetime.life/login.html?resource=%2Fclubs%2Ffl%2Fharbour-island.html")
    page.get_by_role("button", name="Close").click()
    page.get_by_role("textbox", name="Username, Email, or Member ID").click()
    page.get_by_role("textbox", name="Username, Email, or Member ID").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name=" Log In").click()
    page.get_by_role("button", name="Schedules").click()
    page.get_by_role("link", name="Court Reservations").click()
    page.get_by_test_id("resourceBookingFilterBtn").click()
    page.get_by_test_id("sport-toggle").click()
    page.get_by_text("Tennis: Outdoor Court").click()
    page.get_by_test_id("date-toggle").click()

    # Click next week's Tuesday
    tuesday_label = get_next_tuesday_label()
    page.get_by_text(tuesday_label).click()

    page.get_by_test_id("startTime-toggle").click()
    page.get_by_text("6:30 PM").click()
    page.get_by_test_id("duration-toggle").click()
    page.get_by_text("90 Minutes").click()
    page.get_by_test_id("resourceBookingModalApplyFiltersBtn").click()
    page.get_by_role("link", name="6:30 PM Court 5").click()
    page.get_by_test_id("acceptWaiver").locator("span").click()
    page.get_by_test_id("finishBtn").click()

    time.sleep(5)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)