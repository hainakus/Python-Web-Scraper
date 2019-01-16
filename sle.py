import time
from selenium import webdriver

driver = webdriver.Chrome('/usr/bin/chromedriver')  # Optional argument, if not specified will search path.
# or '/usr/lib/chromium-browser/chromedriver' if you use chromium-chromedriver
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()