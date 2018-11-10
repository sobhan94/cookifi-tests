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
from selenium.webdriver.common.action_chains import ActionChains


class Cookifi_bday_test(unittest.TestCase):
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(WidgetTestCase('test_caterer'))
        suite.addTest(WidgetTestCase('test_bday'))
        return suite

    def setUp(self):
        # using Chrome browser. ensure it is installed
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_bday(self):
        driver = self.driver
        # open cookifi site
        driver.implicitly_wait(10)
        driver.get('https://cookifi.com/')
        wait = WebDriverWait(driver, 10)
        # wait for components to be loaded
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "EVENTS")))
        events = driver.find_element_by_partial_link_text('EVENTS')
        birthday = driver.find_element_by_partial_link_text('Birthday')
        ActionChains(driver).move_to_element(events).move_to_element(birthday).click().perform()
        # select a package
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//h3[contains(text(), 'Birthday dinner with Live Counters')])/../..")))
        package = driver.find_element_by_xpath("(//h3[contains(text(), 'Birthday dinner with Live Counters')])/../..")
        package.find_element_by_tag_name('a')
        package.click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[1]//label[1]//select[1]")))
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'LOGIN TO VIEW PRICE')))

        temp = driver.find_element_by_partial_link_text('LOGIN TO VIEW PRICE')
        driver.execute_script("return arguments[0].scrollIntoView();", temp)
        temp.click()
        time.sleep(2)
        driver.find_element_by_partial_link_text('Login with Google').click()
        self.google_login()
        # Fill in the form
        wait.until(EC.presence_of_element_located((By.ID, "id_no_of_people")))
        locality = driver.find_element_by_id('id_locality')
        locality.clear()
        locality.send_keys("testing locality")
        no_of_people = Select(driver.find_element_by_id("id_no_of_people"))
        no_of_people.select_by_visible_text("50")
        # setting the selection for type of meal
        driver.find_element_by_id('id_pure_veg_1').click()
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
        # main menu
        no_of_veg = Select(driver.find_element_by_xpath(
            "//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[1]//label[1]//select[1]"))
        no_of_veg.select_by_visible_text('20')
        no_of_nonveg = Select(driver.find_element_by_xpath(
            "//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[2]//label[1]//select[1]"))
        no_of_nonveg.select_by_visible_text('30')
        driver.find_element_by_partial_link_text('Add Soup').click()
        self.add_bday_dish('Veg Clear Soup', 'Soup')
        self.add_bday_dish('Butter Garlic Prawns', 'Starter')
        self.add_bday_dish('Zafrani pulao', 'Rice')
        self.add_bday_dish('Butter Roti', 'Bread')
        self.add_bday_dish('Chicken Thai Green Curry', 'Main Course')
        self.add_bday_dish('Shahi Tukda', 'Desserts')
        self.add_bday_dish('Sweet Lassi', 'Drinks')
        self.add_bday_dish('Table', 'Add-on')
        # self.add_bday_dish('Bisleri Water Can (20l)', 'Add-on')
        proceed = driver.find_element_by_partial_link_text('PROCEED TO PAYMENT')
        driver.execute_script("return arguments[0].scrollIntoView();", proceed)
        proceed.click()
        # CLICK ON PAYMENT MODE
        payment = driver.find_element_by_xpath("//input[@value='hdfc']")
        payment.click()
        # click for payment
        proceed = driver.find_element_by_xpath("//input[@value='Proceed to payment']").click()

    def test_module(self):
        # declare basic variables
        driver = self.driver
        driver.implicitly_wait(10)
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

    def test_bday(self):
        driver = self.driver
        # open cookifi site
        driver.implicitly_wait(10)
        driver.get('https://cookifi.com/')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Caterer")))
        # click on caterer
        caterer = driver.find_element_by_partial_link_text('Caterer').click()
        # fill form
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        date = driver.find_element_by_id("id_when")
        date.click()
        date.clear()
        date.send_keys(tomorrow.strftime("%Y-%m-%d"))
        date.send_keys(Keys.RETURN)
        #time.sleep(2)
        name = driver.find_element_by_id('id_name')
        name.click()
        name.send_keys('Testing Name')
        location = driver.find_element_by_id('id_location')
        location.click()
        location.send_keys('testing location')
        email = driver.find_element_by_id('id_email')
        email.click()
        email.send_keys('cookifi.test@gmail.com')
        mobile = driver.find_element_by_id('id_mobile')
        mobile.click()
        mobile.send_keys('9833568580')

        submit = driver.find_element_by_id('id_submit')
        #actions = ActionChains(driver)
        #actions.move_to_element(submit).perform()

        driver.execute_script("arguments[0].scrollIntoView();", submit)
        #driver.execute_script("window.scrollBy(0, -20);")
        #time.sleep(4)
        submit.click()

    def google_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        email = 'cookifi.test@gmail.com'
        password = 'testingcookifi'
        wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        driver.find_element_by_id("identifierId").send_keys(email)
        driver.find_element_by_id("identifierNext").click()
        driver.implicitly_wait(10)
        driver.find_element_by_name("password").send_keys(password, Keys.RETURN)

    def add_bday_dish(self, dish, type):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        type_select = Select(driver.find_element_by_xpath("//select[contains(@ng-model, 'selectedCourse')]"))
        type_select.select_by_visible_text(type)
        search = driver.find_element_by_id('add_dish_search')
        search.send_keys(dish)
        dish_select = driver.find_element_by_xpath("(//H4[contains(text()," + "\'" + dish + "\'" + ")])/../../..")
        dish_select.find_element_by_xpath("(//div[contains(@class, 'add_remove_dish')])")
        dish_select.find_element_by_partial_link_text('Add').click()
        # wait.until(EC.presence_of_element_located((By.XPATH, "(//H4[contains(text()," + "\'" + dish + "\'"+ "]/../..//SPAN[@class='added large']")))

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
        self.check_price(str('23,000.00'), item)
        # cutlery set
        item = 'Disposable Set'
        self.add_dish(item)
        self.check_price(str('23,000.00'), item)
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
        self.check_price(str('23,750.00'), item)

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
        # wait.until(EC.presence_of_element_located((By.XPATH, "(//SPAN[contains(text()," + "\'" + item + "\'" + ")])/..//I[@class=\'fa fa-circle-o fv-unselected\']")))
        time.sleep(2)

    def check_price(self, cost, item):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        time.sleep(2)
        # wait.until(EC.presence_of_element_located((By.XPATH, "/span[@class='ng-binding'][contains(text(),"+"\'"+item+"\'"+")]")))
        element = driver.find_element_by_xpath("//td[contains(text(), '₹')]")
        self.assertEqual('₹' + cost, element.text)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
