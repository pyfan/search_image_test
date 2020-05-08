import unittest
import time
import re
from os.path import abspath, dirname, join, basename, splitext
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


CONFIG_FILE = join(dirname(abspath(__file__)), r'./visit.ini')
GOOGLE_URL = r'https://www.google.com'
IMAGE_PATH = join(dirname(abspath(__file__)), r'Donald.jpeg')


def get_image(driver, pic_name):
    '''
    Make a scroll screenshot for whole page in 'headless' mode.
    '''
    # Get the width and height of the whole page in browser
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    
    # Set the values of width and height to window
    driver.set_window_size(width, height)
    time.sleep(1)
   
    driver.save_screenshot(pic_name)


def get_specified_param(pattern, file_path):
    with open(file_path) as f:
        for line in f:
            if pattern in line:
                return int(re.search(r'(\d+)', line).group(0))


class SearchTest(unittest.TestCase):
    def setUp(self):
        # self.firefox_options = Options()
        # self.firefox_options.add_argument('-headless')
        # self.driver = Firefox(options=self.firefox_options)
        self.driver = Firefox()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.close()

    def test_search_by_image(self):
        self.driver.implicitly_wait(120) # to skip the
        self.driver.get(GOOGLE_URL)

        # Open 'Search by Image'.
        self.driver.find_element_by_link_text('Images').click()
        self.driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[3]/div[2]/span').click()
        self.driver.find_element_by_xpath('//*[@id="dRSWfb"]/div/a').click()
        
        # Upload local pic file.
        self.driver.find_element_by_name('encoded_image').send_keys(IMAGE_PATH)       
        
        # Get the relevant results by iteration and visit the specified one in config file.
        results = self.driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div[1]/a/h3')
        visit_number = get_specified_param('VISIT_RESULT', CONFIG_FILE)
        link_text = results[visit_number].text
        print(link_text)
        results[visit_number].click()
        self.driver.save_screenshot('visit_result.png')
        # get_image(self.driver, 'visit_result.png')

        # Validate the results are related to used image.
        search_info, _ = splitext(basename(IMAGE_PATH))
        self.assertIn(search_info, link_text)
        

if __name__ == '__main__':
    unittest.main()

