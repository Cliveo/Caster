import unittest

from castervoice.lib.ctrl.nexus import Nexus
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger

class NoSaveCCRMerger(CCRMerger):
    def save_config(self):
        pass

    def load_config(self):
        self._config = {}

class TestNexus(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.nexus = Nexus(False)
        self.nexus.merger = NoSaveCCRMerger()
