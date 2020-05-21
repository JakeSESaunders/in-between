import unittest
import plugins.base
from xml.etree.ElementTree import Element

class TestBaseHandler(unittest.TestCase):
    def test_a_lru(self):
        login_code, password, name = 'a', 'b', 'c'
        request = Element('a_lru')
        request.set('l', login_code)
        request.set('p', password),
        request.set('n', name)

    def test_a_lgu(self):
        pass

    def test_a_gsd(self):
        pass

    def test_a_gpd(self):
        pass

    def test_a_gsl(self):
        pass

    def test_a_gfl(self):
        pass

    def test_a_alo(self):
        pass

    def test_p(self):
        pass