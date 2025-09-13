from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.details = []
        self.data = []



    def get_data(self, names: list[str], selectors: list[str], types: list[str]):
        self.driver.get(self.url)
        # Se ad una colonna allora rendi tutto visibile ed estrai, se a più colonne allora per ogni colonna assicura che tutto sia visibile e poi estrai.
        # TODO: Scarica pagina
        # if next_page:
            # for _ in range(next_page["clicks"]):
                # TODO: Scarica pagina

        # if external:
            # for detail in details


        # TODO:


    def scrape_page(self, selector: str, more: str | None, internal_details=False) -> None:
        elements = set()
        while True:
            prev_elements_len = len(elements)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for element in soup.select(selector):
                elements.add(element)
            if more and len(elements) != prev_elements_len:
                self.driver.find_element(more).click()
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "myButton")))
            elif internal_details:
                ... #TODO clicca e raccogli i dati in self.data nei dettagli
                return None
            else:
                for element in elements:
                    self.details.append(element.get("href"))
                return None

    def scrape_details(self):
        ...
