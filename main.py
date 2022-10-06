from selenium import webdriver

""" from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options """

import time
from time import gmtime, strftime

from twilio.rest import Client

TWILIO_PHONE_NUMBER = "+177777777"  # Replace with your own Twilio number

DIAL_NUMBERS = [
    "+420777777777",  # Replace with your phone number
]

TWIML_INSTRUCTIONS_URL = "http://static.fullstackpython.com/phone-calls-python.xml"

account = "acc_token"  # Twilio client initialization
token = "token"  # Twilio client initialization

client = Client(account, token)


def dial_numbers(numbers_list):
    for number in numbers_list:
        client.calls.create(
            to=number,
            from_=TWILIO_PHONE_NUMBER,
            url=TWIML_INSTRUCTIONS_URL,
            method="GET",
        )


print("----> Script started...", flush=True)

""" options = Options()
options.headless = True
driver = webdriver.Firefox(options=options) """
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

print("----> Starting the webdriver...", flush=True)
driver.get("https://www.maastrichthousing.com/")

popup = driver.find_element_by_id("step1")
a = popup.find_elements_by_tag_name("a")
a[6].click()

email = driver.find_element_by_id("student_user")
password = driver.find_element_by_id("student_pass")

time.sleep(2)

email.send_keys("email@gmail.com")  # Replace with your email
password.send_keys("********")  # Replace with your password

login = driver.find_element_by_id("login")
button = login.find_element_by_css_selector(
    ".btn.btn-primary.btn-block.btn-lg")
button.click()

print("----> Successfully logged in...", flush=True)

driver.get("https://www.maastrichthousing.com/")

private = driver.find_element_by_id("commercial-checkbox")
private.click()

driver.execute_script(
    "document.getElementById('price').style.display = 'block';")
price = driver.find_element_by_id("price").clear()
price = driver.find_element_by_id("price").send_keys("50,400")

search = driver.find_element_by_css_selector(
    ".btn.btn-primary.btn-lg.btn-block")
search.click()

print("----> Loop started...", flush=True)

with open("newest_room.txt", "r") as f:
    title_first = f.readline().replace("\n", "")

while True:
    time.sleep(10)
    result = driver.find_element_by_id("resultsContainer").find_element_by_css_selector(
        ".listing.col-xs-12.col-sm-12.col-md-6.col-lg-6"
    )
    """ result = driver.find_element_by_id("resultsContainer").find_elements_by_class_name(
        "marker-22"
    ) """

    if len(title_first) == 0:
        title_first = result.get_attribute("title")
        print(
            "----> Initial result checked with the house " + title_first + "...",
            flush=True,
        )
    else:
        if title_first != result.get_attribute("title"):
            # driver.get(result.find_element_by_tag_name("a").get_attribute("href"))
            dial_numbers(DIAL_NUMBERS)
            print(
                "----> "
                + strftime("%Y-%m-%d %H:%M:%S", gmtime())
                + ": "
                + title_first
                + "!="
                + result.get_attribute("title"),
                flush=True,
            )
            with open("newest_room.txt", "w") as f:
                f.write(result.get_attribute("title"))
            title_first = result.get_attribute("title")
        else:
            print(
                "----> "
                + strftime("%Y-%m-%d %H:%M:%S", gmtime())
                + ": No new results ("
                + title_first
                + " == "
                + result.get_attribute("title")
                + ")",
                flush=True,
            )
            with open("newest_room.txt", "w") as f:
                f.write(result.get_attribute("title"))

    time.sleep(40)
    driver.get("https://www.maastrichthousing.com/Search_results.html")
