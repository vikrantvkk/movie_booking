import json

import bookmyshow
import unittest
import tempfile


class BookmyshowTestCase(unittest.TestCase):

    def setUp(self):
        self.db, bookmyshow.app.config['DATABASE'] = tempfile.mkstemp()
        bookmyshow.app.testing = True
        self.app = bookmyshow.app.test_client()

    def tearDown(self):
        pass

    def test_encode(self):
        result = self.app.post('/103021012022/seats')
        result = self.app.post('/u1/103021012022/seats',
                               data='{"seats":["m1s210302101202224", "m1s210302101202225", "m1s210302101202226"]}')
        #
        # assert srt_url == data["short_url"]


if __name__ == '__main__':
    unittest.main()
