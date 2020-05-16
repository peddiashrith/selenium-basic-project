import pytest
import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def scrapedata(driver, data):
	"""
	params are:
	driver: Browser driver
	data: data to added by scraping the present webpage
	"""
	rows = driver.find_elements_by_xpath(
	'//*[@id="main-content-column"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/ng-transclude/table/tbody/tr')
	print("No. of rows are: ", len(rows))
	for row in range(1, 1+len(rows)):
		symbol_element_xpath = '//*[@id="main-content-column"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/ng-transclude/table/tbody/tr[{}]/td[1]/div/span/a'.format(
			row)
		symbol_element = driver.find_element_by_xpath(symbol_element_xpath)
		symbol = symbol_element.text
		name_element_xpath = '//*[@id="main-content-column"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/ng-transclude/table/tbody/tr[{}]/td[2]/div/span/span/span'.format(
			row)
		name_element = driver.find_element_by_xpath(name_element_xpath)
		name = name_element.text
		print(symbol, "\t", name)
		symbol_name_pair = {}
		symbol_name_pair["Symbol"] = symbol
		symbol_name_pair["Name"] = name
		data.append(symbol_name_pair)
	return data


def fetchdata(base_url, keywords):
	"""
	params are:
	base_url: url to be opened first
	keywords: list which contains words to be searched for
	"""
	driver = webdriver.Chrome(executable_path="chromedriver.exe")
	driver.get("https://www.barchart.com/stocks/quotes/GOOG/competitors")
	driver.implicitly_wait(20)
	data = []  # To store the data in dictionary format
	for symbol in keywords:
		driver.find_element(By.ID, "search").click()
		driver.find_element(By.ID, "search").send_keys(symbol)
		# wait till the all the search results appear
		driver.implicitly_wait(20)
		driver.find_element_by_xpath(
			'//*[@id="bc-main-content-wrapper"]/div/div[1]/div[1]/div/div/div[6]/div[1]/div/a/div/div[1]/span').click()
		# wait till all elements of the page are loaded
		driver.implicitly_wait(20)
		scrapedata(driver, data)
	return data


def give_keywords(filename="keywords.txt"):
    keywords = []
    inputfile = open(filename)
    # assuming only one symbol per line
    for symbol in inputfile:
        symbol = symbol.rstrip("\n")
        keywords.append(symbol)
        print(symbol)
    return keywords


def write_to_outputfile(data, filename="output.json"):
    with open(filename, 'w') as fout:
        json.dump(data, fout, indent=4)
    return


if __name__ == "__main__":
    keywords = give_keywords(sys.argv[1])
    base_url = "https://www.barchart.com/stocks/quotes/GOOG/competitors"
    data = fetchdata(base_url, keywords)
    write_to_outputfile(data)
