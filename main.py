from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service



URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64481581640625%2C%22east%22%3A-122.22184218359375%2C%22south%22%3A37.69519429240501%2C%22north%22%3A37.85530193111828%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
FORM_URL = "https://docs.google.com/forms/d/1ugjLokFnZEW31BEU4uRH-NzhGhyQ85cXfY91EbP8Dr4/viewform?edit_requested=true&fbzx=7118870202003034370"
class RealEstateEntryBot:
    def __init__(self):
        chrome_driver_path = "C:\Development\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.soup = ""
        self.driver.implicitly_wait(5)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_real_estate_data(self):

        self.driver.get(URL)
        self.driver.maximize_window()
        all_lists = []

        flag = True

        while flag:
            all_lists = self.driver.find_elements(by=By.XPATH, value='//div[@id="grid-search-results"]/ul/li[not(p)]')

            try:
                all_lists[-1].find_element(by=By.TAG_NAME, value="address")
            except StaleElementReferenceException or NoSuchElementException:
                ActionChains(self.driver).move_to_element(all_lists[-1])
            else:
                flag = False

        # print(all_lists[0].find_element(by=By.TAG_NAME, value="address").text)

        all_address = [link.find_element(by=By.TAG_NAME, value="address").text for link in all_lists]
        all_prices = [link.find_element(by=By.CSS_SELECTOR, value='span[data-test="property-card-price"]').text for link in all_lists]
        all_links = [link.find_element(by=By.CLASS_NAME, value='property-card-link').get_attribute("href") for link in all_lists]

        # print(all_address)
        # print(all_prices)
        # print(all_links)

        all_data = [all_address, all_prices, all_links]
        return all_data


    def fill_form(self, data):
        self.driver.get(FORM_URL)
        input_boxes = self.driver.find_elements(by=By.CSS_SELECTOR, value="input.whsOnd")
        for to_fill, box in zip(data, input_boxes):
            box.click()
            box.send_keys(to_fill)

        self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Submit')]").click()


Bot = RealEstateEntryBot()
all_data = Bot.get_real_estate_data()

address = all_data[0]
price = all_data[1]
link = all_data[2]

for (a, p, l) in zip(address, price, link):
    data = [a, p, l]
    Bot.fill_form(data)

