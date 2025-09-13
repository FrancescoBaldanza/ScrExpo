from dataset import Dataset
from bs4 import BeautifulSoup, PageElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# TODO: funzione che restitusca l'url assoluto invece di quello relativo

class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.data = []


    def get_data(self, dataset: Dataset):
        self.driver.get(dataset.url)
        if dataset.detail_pages.external:
            details_pages = self.scrape_pages(dataset.detail_pages.selector, dataset.more)
            if dataset.next_page:
                for _ in range(dataset.next_page["clicks"]):
                    details_pages.extend(self.scrape_pages(dataset.detail_pages.selector, dataset.more))

            for page in details_pages:
                ...



    def scrape_pages(self, selector: str, more: str | None) -> list[PageElement]:
        elements = set()
        while True:
            prev_elements_len = len(elements)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for element in soup.find_all(selector):
                element = element.get("href")
                elements.add(element)
            if more and len(elements) != prev_elements_len:
                self.driver.find_element(more).click()
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "myButton")))
            else:
                return list(elements)


    def scrape_details(self):
        ...
