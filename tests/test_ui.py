import unittest
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestUI(unittest.TestCase):
    def setUp(self):
        self.response = requests.get('http://localhost:5000')
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        self.driver.quit()

    def test_background_color(self):
        style_tag = self.soup.find('style')
        self.assertIn('background-color: #E0F7FA', style_tag.text)

    def test_dog_box(self):
        dog_box = self.soup.find('div', class_='dog-box')
        self.assertIsNotNone(dog_box)
        self.assertIn('position: fixed', dog_box['style'])
        self.assertIn('bottom: 0', dog_box['style'])
        self.assertIn('left: 0', dog_box['style'])
        self.assertIn('width: 200px', dog_box['style'])
        self.assertIn('height: 200px', dog_box['style'])
        self.assertIn('background-color: #FFFFFF', dog_box['style'])
        self.assertIn('border: 2px solid #262626', dog_box['style'])
        self.assertIn('border-radius: 10px', dog_box['style'])
        self.assertIn('padding: 10px', dog_box['style'])
        self.assertIn('box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 8px 0px', dog_box['style'])
        self.assertIn('z-index: 1000', dog_box['style'])

        dog_image = dog_box.find('img')
        self.assertIsNotNone(dog_image)
        self.assertIn('width: 100%', dog_image['style'])
        self.assertIn('height: 100%', dog_image['style'])
        self.assertIn('object-fit: cover', dog_image['style'])
        self.assertIn('border-radius: 10px', dog_image['style'])

if __name__ == '__main__':
    unittest.main()

