from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def write_to_file(text):
    f = open("weblog.txt", "a")
    f.write(text)
    f.close()


def test_selenium():
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome('/usr/local/bin/chromedriver',  options=chrome_options)

    driver.get("http://www.python.org")

    write_to_file(driver.title)
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
