import time

from scraping import Scraper
import pandas as pd


def scrape_infos():
    chrome = Scraper('https://www.viki.com/?locale=fr')
    chrome.access_website()
    chrome.accept_cookies()
    chrome.click_on_by_xpath("//span[text()='Explorer']")
    chrome.click_on_by_xpath("//a[text()='Tous les spectacles']")
    chrome.click_on_by_xpath("//span[text()='Tous les types']")
    chrome.click_on_by_xpath("//div[text()='Télévision']")
    series = chrome.get_all_shows(50, 'Série')
    time.sleep(10)
    chrome.click_on_by_xpath("//span[text()='Télévision']")
    chrome.click_on_by_xpath("//div[text()='Films']")
    movies = chrome.get_all_shows(3, 'Film')
    chrome.quit_driver()
    shows = series + movies
    return shows


def to_csv(shows):
    df_shows = pd.DataFrame(shows)
    df_shows.to_csv('viki_shows.csv', index=False)


if __name__ == "__main__":
    to_csv(scrape_infos())
