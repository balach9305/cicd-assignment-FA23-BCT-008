"""Four browser tests required for CSC418 Lab Assignment 3."""
import os
import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8091")
EXPECTED_ROLL = "FA23-BCT-008"


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    options.add_argument(f"--user-data-dir=/tmp/chrome-{uuid.uuid4().hex}")
    browser = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"), options=options
    )
    yield browser
    browser.quit()


def test_title_contains_roll_number(driver):
    driver.get(BASE_URL)
    assert driver.title == f"CI/CD Assignment 3 | {EXPECTED_ROLL}"
    assert "YOUR_" not in driver.title


def test_heading_and_student_details(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "main-heading").text
    assert heading == f"Automated CI/CD Pipeline — {EXPECTED_ROLL}"
    assert "Balach Khan" in driver.find_element(By.ID, "student-name").text
    assert EXPECTED_ROLL in driver.find_element(By.ID, "roll-number").text


def test_button_click_displays_greeting(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "button-message"), "Hello")
    )
    assert driver.find_element(By.ID, "button-message").text == "Hello from Balach Khan!"


def test_textbox_input_and_centered_submission(driver):
    driver.get(BASE_URL)
    typed_message = "Selenium input test passed"
    field = driver.find_element(By.ID, "message-input")
    field.send_keys(typed_message)
    assert field.get_attribute("value") == typed_message
    driver.find_element(By.ID, "submit-btn").click()
    output = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "submitted-text"), typed_message)
    )
    assert output is True
    result = driver.find_element(By.ID, "submitted-text")
    assert result.text == typed_message
    assert result.value_of_css_property("text-align") == "center"
    driver.save_screenshot("screenshot.png")
