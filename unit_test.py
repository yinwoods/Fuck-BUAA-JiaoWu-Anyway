import unittest
from crawler import Crawler

class Test(unittest.TestCase):

    def setUp(self):
        self.cw = Crawler()

    def test_get_verify_code(self):
        with open('verify.txt', 'r') as f:
            verifyCode = f.read()


        print(self.cw.filter_verify_code(verifyCode))
        #self.assertEqual(True, True)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
