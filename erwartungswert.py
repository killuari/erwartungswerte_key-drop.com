from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options, executable_path=r'E:\Programmieren\Python\Selenium\driver\chromedriver.exe')
delay = 3

def erwartungswertBerechnen(caseURL):
    driver.get(caseURL)
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='case-root']/div/section/ul")))

    odds_button = driver.find_element(By.XPATH, "//*[@id='case-root']/div/section/div/div/button")
    odds_button.click()
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='odds-range-modal']/div/div/div/div[2]/table/tbody")))

    price = driver.find_element(By.XPATH, "//*[@id='odds-range-modal']/div/div/div/div[1]/div/div[2]/div/div").text
    float_price = float(price.split()[0].replace(",", "").strip("$"))

    odds_range = driver.find_elements(By.XPATH, "//*[@id='odds-range-modal']/div/div/div/div[2]/table/tbody/tr")

    odds = []
    odds_float = []
    prices = []
    prices_float = []
    gewinn = []
    erwartungswert_gewinn = 0
    erwartungswert = 0
    varianz = 0

    for i in range(1, len(odds_range)+1):
        prices.append(driver.find_element(By.XPATH, "//*[@id='odds-range-modal']/div/div/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]").text)
        odds.append(driver.find_element(By.XPATH, "//*[@id='odds-range-modal']/div/div/div/div[2]/table/tbody/tr[" + str(i) + "]/td[4]").text)

    for i in range(len(prices)):
        prices_float.append(float(prices[i].split()[0].replace(",", "").strip("$")))
        gewinn.append(prices_float[i] - float_price)

    for i in range(len(odds)):
        float_odd = (float(odds[i].replace(",", ".").strip("%")))
        odds_float.append(float_odd/100)

    for i in range(len(odds_range)):
        erwartungswert_gewinn += gewinn[i] * odds_float[i]
        erwartungswert += prices_float[i] * odds_float[i]

    for i in range(len(odds_range)):
        varianz += (prices_float[i] * erwartungswert)**2 * odds_float[i]
    standardabweichung = math.sqrt(varianz)

    erwartungswert_gewinn_prozentual = round(erwartungswert_gewinn/float_price*100, 1)

    file1 = open("E:\Programmieren\Python\Selenium\keydrop\erwartungswerte.txt", "a")
    file1.write(caseURL.split("/")[-1].capitalize() + ":\n")
    file1.write("Erwartungswert: $" + str(round(erwartungswert, 2)) + "\n")
    file1.write("Standardabweichung: " + str(round(standardabweichung, 2)) + "\n")
    file1.write("Gewinnerwartung: $" + str(round(erwartungswert_gewinn, 2)) + " - " + str(erwartungswert_gewinn_prozentual) + "%\n\n")
    file1.close()

    print(caseURL.split("/")[-1].capitalize() + " done!")

def alleCasesDurchgehen():
    file1 = open("E:\Programmieren\Python\Selenium\keydrop\erwartungswerte.txt", "w")
    file1.write("")
    file1.close()
    driver.get("https://key-drop.com/")
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cs-go-heroes']/div[2]/div[2]/a")))

    hrefs=[]
    case_sections = ["'limited-edition'", "'legacy'", "'cs-go-kings'", "'cs-go-cage'", "'cs-go-magic'", "'cs-go-heroes'", "'cs-go-premium'", "'cs-go-skins'", "'cs-go-guns'"]

    for l in case_sections:
        section = driver.find_elements(By.XPATH, "//*[@id=" + l + "]/div[2]/div")
        for i in range(1, len(section)+1):
            hrefs.append(driver.find_element(By.XPATH, "//*[@id=" + l + "]/div[2]/div[" + str(i) + "]/a").get_attribute("href"))

    # youtubers cases einzeln hinzufuegen
    section = driver.find_elements(By.XPATH, "//*[@id='youtubers-cases']/div[2]/div")
    for i in range(2, len(section)+1):
        hrefs.append(driver.find_element(By.XPATH, "//*[@id='youtubers-cases']/div[2]/div[" + str(i) + "]/a").get_attribute("href"))

    for url in hrefs:
        erwartungswertBerechnen(url)

alleCasesDurchgehen()