from dataset import Dataset
from bs4 import BeautifulSoup, PageElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dataset import Dataset


def get_performance_logs_and_check_for_500(driver: webdriver.Chrome) -> bool:
    """
    Cattura i log di performance del browser e verifica la presenza di errori 500.

    Args:
        driver: L'istanza del WebDriver.

    Returns:
        bool: True se viene trovato un errore 500, altrimenti False.
    """
    try:
        logs = driver.get_log('performance')
        for entry in logs:
            try:
                message_data = json.loads(entry['message'])
                # Controlla se il messaggio è una risposta di rete
                if 'Network.responseReceived' in message_data['message']['method']:
                    response = message_data['message']['params']['response']
                    if response['status'] == 500:
                        print(f"❌ Errore 500 rilevato per l'URL: {response['url']}")
                        return True
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print(f"Errore durante la cattura dei log: {e}")
    return False

def scrape_with_error_check(url: str, button_selector: str, max_clicks: int=30) -> list[str]:
    """
    Scrapa una pagina cliccando un bottone e si ferma in caso di errore 500.

    Args:
        url (str): L'URL della pagina da scrapare.
        button_selector (str): Il selettore CSS per il bottone.
        max_clicks (int): Il numero massimo di tentativi di clic.
    """
    # Configura il WebDriver per catturare i log di performance
    capabilities = webdriver.DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    # Inizializza il driver con le capabilities
    driver = webdriver.Chrome(desired_capabilities=capabilities)

    try:
        print(f"Caricamento della pagina: {url}")
        driver.get(url)
        time.sleep(2)  # Pausa per permettere il caricamento iniziale

        click_count = 0
        while click_count < max_clicks:
            # Step 1: Controlla i log prima di ogni clic
            if get_performance_logs_and_check_for_500(driver):
                print("Interruzione del processo a causa di un errore del server.")
                break

            try:
                # Step 2: Trova e clicca sul bottone "carica altro"
                wait = WebDriverWait(driver, 10)
                load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))

                print(f"Cliccando il botton.e 'carica altro' (tentativo {click_count + 1}).")
                driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                time.sleep(1)
                load_more_button.click()
                click_count += 1
                time.sleep(2)  # Pausa per permettere il caricamento

            except (TimeoutException, NoSuchElementException):
                print("Nessun altro bottone 'carica altro' trovato. Tutti i contenuti sono caricati.")
                break

    finally:
        # Step 3: Pulisci e chiudi il browser
        driver.quit()
        print("Driver chiuso.")

# TODO: scrape_urls()
# TODO: scrape_details()
# TODO:

# se esterno
    # se piu pagine:
        # per n-1 volte:
            # se bottone:
                # carichi elementi tutti gli elementi fino ad EVENTO UNICO
            # scarichi gli urls (trovi gli elementi e selezioni gli href)
            # passi alla prossima pagina (clicchi su next_page n-1 volte)
    # per ogni pagina di dettagli (
    # scarichi i dettagli
#

def absolute_url(home: str, child: str) -> str:
    from urllib.parse import urljoin, urlparse
    parsed_child = urlparse(child)
    if parsed_child.scheme and parsed_child.netloc:
        return child
    return urljoin(home, child)

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
