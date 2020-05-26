import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command

from captcha import initiateCaptchaRequest, requestCaptchaResults
from check_download_complete import every_downloads_chrome
from remove_files import remove_books


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from PyInquirer import prompt
from choice_book import choice_book
from upload_file import upload
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import config

# How to save and load cookies using Python + Selenium WebDriver

# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
chrome_options = Options()
chrome_options.headless = True
#chrome_options.add_argument("--no-sandbox")  # linux only
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--timeout 30000")
chrome_options.add_argument("--dns-prefetch-disable")



options = FirefoxOptions()
options.add_argument("--no-sandbox")  # linux only
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
#driver = webdriver.Firefox(options=options)
books_dict = {}


def add_book_option(book):
    book_option = book.text.replace("Baixar ou Ler Online", "")
    if (book_option != ""):
        books_dict[book_option] = book
        choice_book[0]['choices'].append(book_option)


def search_book():
    driver.get("http://lelivros.love/")
    book_search = input("Qual o livro: ")
    search_form = driver.find_elements_by_xpath("//input[@name='s']")[0]
    search_form.clear()
    search_form.send_keys(book_search)
    search_form.send_keys(Keys.RETURN)
    wait = WebDriverWait(driver, 10)
    books = wait.until(EC.presence_of_all_elements_located(('xpath', "//ul//li[contains(@class,'post')]//a")))
    [add_book_option(book) for book in books]
    answer = prompt(choice_book)
    download_book(books_dict[answer["book"]].get_attribute("href"))


def requesting_download(url):
    print("Requesitando o Download")
    driver.get(url)
    buttom_link = driver.find_elements_by_xpath("//img[contains(@alt, 'Baixar em mobi')]")[0]
    #driver.set_page_load_timeout(1000)
    driver.execute(Command.SET_TIMEOUTS, {
        'ms': float(1000),
        'type': 'page load'})
    buttom_link.click()
    driver.implicitly_wait(3)
    driver.switch_to.window(driver.window_handles[1])

def waiting_download():
    print("Esperando Liberar o Download")
    buttom_download = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located(("xpath","//div[@class='download-timer']//a")))
    buttom_download.click()
    driver.implicitly_wait(10)

def bypass_captcha():
    print("Passando pelo captcha")
    siteKey = driver.find_element_by_xpath("//div[@data-sitekey]").get_attribute("data-sitekey")
    request_id = initiateCaptchaRequest(config.apiKey, siteKey, driver.current_url)
    response = requestCaptchaResults(config.apiKey, request_id)
    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML="{0}";'.format(response))
    time.sleep(4)
    continue_button = driver.find_element_by_id("submit")
    continue_button.click()
    time.sleep(4)

def check_captcha():
    print("checking captcha invalid")

def download_book(url):
    requesting_download(url)
    waiting_download()
    bypass_captcha()
    print("Fazendo download")
    paths = WebDriverWait(driver, 1200, 1).until(every_downloads_chrome)
    driver.quit()


if __name__ == '__main__':
    search_book()
    upload()
    remove_books()