from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


class Scraper:
    def __init__(self, url):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--window-size=1420,1080')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.url = url

    def access_website(self):
        self.driver.get(self.url)
        time.sleep(20)

    def click_on_by_text(self, text):
        self.driver.find_element_by_link_text(text).click()

    def click_on_by_xpath(self, xpath):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def click_on_by_id(self, id_name):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, id_name))).click()

    def accept_cookies(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept All']"))).click()
        time.sleep(10)

    def get_show(self, results, category):
        all_widgets = self.driver.find_elements_by_class_name("explore-results")
        first_line = all_widgets[0]
        all_first_line_elements = first_line.find_elements_by_class_name('col-inline')
        all_first_line_images = first_line.find_elements_by_css_selector('img.responsive-img')
        for i in range(len(all_first_line_elements)):
            try:
                show = all_first_line_elements[i].text.split('\n')
                details = show[1].split('•')
                votes_details = details[1].split('(')
                image = all_first_line_images[i].get_attribute('src')
                results.append({'Type': category, 'Nom': show[0], 'Pays': details[0], 'Note': votes_details[0],
                                'Nb_votes': votes_details[1].split(' ')[0], 'image': image})
            except:
                continue
        return results

    def get_all_shows(self, pages, category):
        results = []
        for i in range(pages):
            try:
                self.get_show(results, category)
                WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[text()='Suivant →']"))).click()
            except:
                continue
        return results

    def quit_driver(self):
        self.driver.quit()


def scrape_infos():
    chrome = Scraper('https://www.viki.com/?locale=fr')
    chrome.access_website()
    chrome.accept_cookies()
    chrome.click_on_by_xpath("//span[text()='Explorer']")
    chrome.click_on_by_xpath("//a[text()='Tous les spectacles']")
    chrome.click_on_by_id("select2-chosen-2")
    chrome.click_on_by_xpath("//div[text()='Télévision']")
    series = chrome.get_all_shows(50, 'Série')
    time.sleep(20)
    chrome.click_on_by_xpath("//span[text()='Télévision']")
    time.sleep(10)
    chrome.click_on_by_xpath("//div[text()='Films']")
    time.sleep(20)
    movies = chrome.get_all_shows(3, 'Film')
    chrome.quit_driver()
    shows = series + movies
    return shows


def to_csv(shows):
    df_shows = pd.DataFrame(shows)
    df_shows.to_csv('viki_shows.csv', index=False)
    print('Scraping done')
