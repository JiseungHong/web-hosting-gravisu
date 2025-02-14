import unittest

class TestStyleCSS(unittest.TestCase):

    def test_background_color(self):
        with open('style.css', 'r') as f:
            content = f.read()
            self.assertIn('background-color: #87CEEB;', content)

if __name__ == '__main__':
    unittest.main()
