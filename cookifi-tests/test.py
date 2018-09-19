import time
import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from unicodedata import decimal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Cookifi_testing_Module(unittest.TestCase):
    def setUp(self):
        # using Chrome browser. ensure it is installed
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_module(self):
        # declare basic variables
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # opening Cookifi website
        driver.get("https://cookifi.com/")
        # wait for the large gathering button to be loaded
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "LARGE GATHERING")))
        # find and click on large gatherings
        driver.find_element_by_partial_link_text("LARGE GATHERING").click()
        # select the plan you want to choose, change the name to click on another.
        # cookifi value non-veg has been considered here
        wait.until(EC.presence_of_element_located((By.XPATH, "//H3[text()='Cookifi Value Non Veg']/../..")))
        package = driver.find_element_by_xpath("//H3[text()='Cookifi Value Non Veg']/../..")
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "CHOOSE DISHES")))
        package.find_element_by_link_text("CHOOSE DISHES").click()

        # Login to view prices. we will be using Google login here
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Login with Google")))
        driver.find_element_by_partial_link_text("Login with Google").click()
        # Login with Google
        # the email and password fields can be replaced to suit the users needs
        self.google_login()
        # Fill in the form
        wait.until(EC.presence_of_element_located((By.ID, "id_no_of_people")))
        locality = driver.find_element_by_id('id_locality')
        locality.clear()
        locality.send_keys("testing locality")
        no_of_people = Select(driver.find_element_by_id("id_no_of_people"))
        no_of_people.select_by_visible_text("50")
        # setting the date of the event, the current date as been set for tomorrow.
        # it can be changed later
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        date = driver.find_element_by_id("id_date")
        date.click()
        date.clear()
        date.send_keys(tomorrow.strftime("%Y-%m-%d"))
        # Se;ect meal
        meal = Select(driver.find_element_by_id("id_meal"))
        meal.select_by_visible_text("Lunch")
        form = driver.find_element_by_id("sendform")
        form.submit()
        # No of people
        #   no of veg
        no_of_veg = Select(driver.find_element_by_xpath(
            "//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[1]//label[1]//select[1]"))
        no_of_veg.select_by_visible_text('20')
        #   no of nonbeg
        no_of_noneg = Select(driver.find_element_by_xpath(
            "//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[2]//label[1]//select[1]"))
        no_of_noneg.select_by_visible_text('30')
        # Add Dishes
        self.fill_menu()
        # assert value
        # proceed to payment
        proceed = driver.find_element_by_partial_link_text('PROCEED TO PAYMENT')
        proceed.click()
        # CLICK ON PAYMENT MODE
        payment = driver.find_element_by_xpath("//input[@value='hdfc']")
        payment.click()
        # click for payment
        proceed = driver.find_element_by_xpath("//input[@value='Proceed to payment']")
        proceed.click()

    def google_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        email = 'cookifi.test@gmail.com'
        password = 'mitu4555'
        wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        driver.find_element_by_id("identifierId").send_keys(email)
        driver.find_element_by_id("identifierNext").click()
        driver.implicitly_wait(10)
        driver.find_element_by_name("password").send_keys(password, Keys.RETURN)

    def fill_menu(self):
        # starter selected = Hara Bhara Kebab
        item = 'Hara Bhara Kebab'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        item = 'Chicken Kebab'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        # dal selected = Dal Tadka
        item = 'Dal Tadka'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        # Gravy Main Couse
        item = 'Patiala Murgh'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        item = 'Butter Chicken'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        # Rice
        item = 'Vegetable Pulao'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        # Bread
        item = 'Butter Roti'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        # Deserts
        item = 'Shahi Tukda'
        self.add_dish(item)
        self.check_price(str('20,000.00'), item)
        # live counter
        item = 'Pizza Live counter'
        self.add_dish(item)
        self.check_price(str('25,500.00'), item)
        # cutlery set
        item = 'Disposable Set'
        self.add_dish(item)
        self.check_price(str('25,500.00'), item)
        # Complementary select 5
       # item = 'Fried Papad'
       # self.add_dish(item)
       # self.check_price(str('25,500.00'), item)
       # item = 'Indian Green Salad'
       # self.add_dish(item)
       # self.check_price(str('25,500.00'), item)
       # item = 'Water Can'
       # self.add_dish(item)
       # self.check_price(str('25,500.00'), item)
       # item = 'Mixed salad raita'
       # self.add_dish(item)
       # self.check_price(str('25,500.00'), item)
       # item = 'Mixed Pickle'
       # self.add_dish(item)
       # self.check_price(str('25,500.00'), item)
        # Welcome  drink
        item = 'Mojito'
        self.add_dish(item)
        self.check_price(str('26,500.00'), item)

    def add_dish(self, item):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text()," + "\'" + item + "\'" + ")]/ancestor::DIV[contains(@class, 'fv-group-dish')]")))
        new_dish = driver.find_element_by_xpath(
            "//span[contains(text()," + "\'" + item + "\'" + ")]/..")
        try:
            if new_dish.find_element_by_xpath("(//I[@class='fa fa-circle-o fv-unselected'])/.."):
                new_dish.find_element_by_tag_name('a').click()
        except NoSuchElementException:
            print('...')
        wait.until(EC.presence_of_element_located((By.XPATH, "(//SPAN[contains(text()," + "\'" + item + "\'" + ")])/..//I[@class=\'fa fa-circle-o fv-unselected\']")))
        time.sleep(1)

    def check_price(self, cost, item):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # wait.until(EC.presence_of_element_located((By.XPATH, "/span[@class='ng-binding'][contains(text(),"+"\'"+item+"\'"+")]")))
        element = driver.find_element_by_xpath("//td[contains(text(), '₹')]")
        self.assertEqual('₹' + cost, element.text)


if __name__ == '__main__':
    unittest.main()
