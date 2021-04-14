from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        time.sleep(10)

    def click_on_by_text(self, text):
        self.driver.find_element_by_link_text(text).click()

    def click_on_by_xpath(self, xpath):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def accept_cookies(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))).click()
        time.sleep(10)

    def get_show(self, results, category):
        all_widgets = self.driver.find_elements_by_class_name("explore-results")
        first_line = all_widgets[0]
        all_first_line_elements = first_line.find_elements_by_class_name('col-inline')
        for element in all_first_line_elements:
            try:
                show = element.text.split('\n')
                details = show[1].split('•')
                votes_details = details[1].split('(')
                results.append({'Type': category, 'Nom': show[0], 'Pays': details[0], 'Note': votes_details[0],
                                'Nb_votes': votes_details[1].split(' ')[0]})
            except:
                continue
        return results

    def get_all_shows(self, pages, category):
        results = []
        for i in range(pages):
            try:
                self.get_show(results, category)
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[text()='Suivant →']"))).click()
            except:
                continue
        return results

    def quit_driver(self):
        self.driver.quit()
