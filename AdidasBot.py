#!/usr/bin/env python3

"""
    *******************************************************************************************
    AliLab.
    Author: Ali Toori, Python Developer [Web-Automation Bot Developer | Web-Scraper Developer]
    Profiles:
        Upwork: https://www.upwork.com/freelancers/~011f08f1c849755c46
        Fiver: https://www.fiverr.com/alitoori
    *******************************************************************************************
"""
import os
import time
import random
import ntplib
import datetime
import pyfiglet
import pandas as pd
import logging.config
from time import sleep
import concurrent.futures
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, UnableToSetCookieException


class Adidas:

    def __init__(self):
        self.PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        pass

    # Get random user-agent
    def get_random_user_agent(self):
        user_agents_list = []
        with open('user_agents.txt') as f:
            content = f.readlines()
        user_agents_list = [x.strip() for x in content]
        return random.choice(user_agents_list)

    # Get random proxy
    def get_random_proxy(self):
        proxies_list = []
        with open('proxies.txt') as f:
            content = f.readlines()
        proxies_list = [x.strip() for x in content]
        return random.choice(proxies_list)

    def get_product(self, shipping):
        # For MacOS chromedriver path
        # PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        # DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(F'--user-agent={self.get_random_user_agent()}')
        # options.add_argument('--headless')
        # driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options)
        driver = webdriver.Chrome(options=options)
        actions = ActionChains(driver)
        # The main homepage URL (AKA base URL)ere
        main_url = 'https://www.adidas.com/us'
        product_bought = False
        # Login to the website
        # self.login()
        item_url = shipping["ProductURL"]
        item_size = str(shipping["ShoeSize"])
        print('[Item URL]:', item_url)
        print('[Processing product add-to-cart]')
        print('[Your selected size]:', item_size)
        # WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CLASS_NAME, 'top-header-link')))
        while product_bought is False:
            # Wait for 1500 mSeconds
            sleep(1.5)
            driver.get(url=item_url)
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'gl-icon')))
                driver.find_element_by_class_name('gl-icon').click()
            except:
                pass
            driver.find_element_by_tag_name('html').send_keys(Keys.SPACE)
            try:
                WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div[3]/div[2]/div[2]/section/div[1]/div[2]')))
            except:
                pass
            print('Available Sizes:', str(driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[3]/div[2]/div[2]/section/div[1]/div[2]').text).strip().split('\n'))
            for label in driver.find_elements_by_css_selector('.gl-label.size___2Jnft'):
                if str(label.text).strip() == item_size:
                    actions.move_to_element(label).click().perform()
                    print('Product size selected:', str(label.text).strip())
                    break
                else:
                    continue
            try:
                # Wait for Ad-To-Cart button to be visible and click
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div/div/div[3]/div[2]/div[2]/section/div[3]/button')))
                add_to_cart = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div/div/div/div[3]/div[2]/div[2]/section/div[3]/button')
                actions.move_to_element(add_to_cart)
                add_to_cart.click()
            except WebDriverException as exc:
                # Wait for Ad-To-Cart button to be visible and click
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'buy-section___ZPaYL')))
                add_to_cart = driver.find_element_by_class_name('buy-section___ZPaYL').find_element_by_tag_name('button')
                actions.move_to_element(add_to_cart)
                add_to_cart.click()
            try:
                # Wait for close button to be visible and click
                WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CLASS_NAME, 'gl-modal__close')))
                driver.find_element_by_class_name('gl-modal__close').click()
            except:
                pass
            # Checkout
            # try:
            # Delivery
            print('Checking out...')
            driver.get(url=main_url + '/delivery')
            if self.first_time:
                WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.NAME, 'firstName')))
                driver.find_element_by_name('firstName').send_keys(shipping['FirstName'])
                driver.find_element_by_name('lastName').send_keys(shipping['LastName'])
                sleep(0.1)
                driver.find_element_by_name('address1').send_keys(shipping['Street'])
                driver.find_element_by_name('city').send_keys(shipping['City'])
                sleep(0.1)
                select = Select(driver.find_element_by_name('stateCode'))
                # select state by visible text
                select.select_by_visible_text(shipping['State'])
                sleep(0.1)
                zip_code = driver.find_element_by_name('zipcode')
                actions.move_to_element(zip_code)
                zip_code.send_keys(str(shipping['ZipCode']))
                # driver.find_element_by_tag_name('html').send_keys(Keys.END)
                sleep(0.1)
                phone_number = driver.find_element_by_name('PhoneNumber')
                actions.move_to_element(phone_number)
                phone_number.send_keys(str(shipping['phone']))
                email = driver.find_element_by_name('emailAddress')
                actions.move_to_element(email)
                email.send_keys(shipping['EmailAddress'])
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gl-cta.gl-cta--primary')))
            pay = driver.find_element_by_css_selector('.gl-cta.gl-cta--primary')
            actions.move_to_element(pay)
            pay.click()
            sleep(3)
            print('Payment processing...')
            # Payment
            if self.first_time:
                WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.NAME, 'card.number')))
                card_num = driver.find_element_by_name('card.number')
                card_num.send_keys(str(shipping['CardNumber']))
                card_expiry = driver.find_element_by_css_selector('.wpwl-control.wpwl-control-expiry.gl-input__field')
                card_expiry.send_keys(str(shipping['CardExpiry']))
                sleep(0.1)
                driver.find_element_by_name('card.cvv').send_keys(str(shipping['CVV']))
                self.first_time = False
            driver.find_element_by_tag_name('html').send_keys(Keys.END)
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div/main/button')))
            buy = driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[2]/div/main/button')
            actions.move_to_element(buy)
            buy.click()
            sleep(3)
            print('Confirming the payment...')
            product_bought = True
            # Order Complete
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.step__label___36A7z.gl-label.gl-label--m.gl-label--bold')))
            #
            # except WebDriverException as exc:
            #     continue
            # Add item to Used Items
            self.to_file(r'AdidasRes\Used_Items.txt', item_url)
            # Close and quit the browser
            self.finish(driver=driver)

    def to_file(self, filename, row):
        with open(filename, "a+") as file:
            file.write(row + '\n')

    def finish(self, driver):
        try:
            driver.close()
            driver.quit()
        except WebDriverException as exc:
            print('Error in closing WebDriver instance ...', exc.args)


def main():
    adidas = Adidas()
    # try:
    file_path_shipping = os.path.join(adidas.PROJECT_ROOT, 'AdidasRes\ShippingDetails.csv')
    if os.path.isfile(file_path_shipping):
        df = pd.read_csv(file_path_shipping, index_col=None)
        num_workers = len(df)
        shipping_list = []
        for shipping in df.iloc:
            shipping_list.append(shipping)
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            executor.map(adidas.get_product, shipping_list)

    else:
        print('ProductLinks is empty. size:', str(os.path.getsize(file_path_shipping).real) + 'KB')
    # except WebDriverException as exc:
    #     print('Exception in WebDriver:', exc.msg)
    #     adidas.finish()

# Trial version logic
def trial(trial_date):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org')
    local_time = time.localtime(response.ref_time)
    current_date = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
    return trial_date > current_date


if __name__ == '__main__':
    trial_date = datetime.datetime.strptime('2020-09-04 03:20:00', '%Y-%m-%d %H:%M:%S')
    # Print ASCII Art
    print('************************************************************************\n')
    pyfiglet.print_figlet('____________               AdidasBot ____________\n', colors='RED')
    print('Author: Ali Toori, Python Developer [Web-Automation Bot Developer]\n'
          'Profiles:\n\tUpwork: https://www.upwork.com/freelancers/~011f08f1c849755c46\n\t'
          'Fiver: https://www.fiverr.com/alitoori\n************************************************************************')
    # Trial version logic
    if trial(trial_date):
        print("Your trial will end on: ", str(trial_date) + ".\n To get full version, please contact fiverr.com/AliToori !")
        main()
    else:
        print("Your trial has been expired, To get full version, please contact fiverr.com/AliToori !")