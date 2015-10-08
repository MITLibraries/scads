import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from models import Workflow

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_workflow_init_defaults(self):
        workflow = Workflow(name="Richard's WF")
        self.assertEqual(1, workflow.version)

if __name__ == '__main__':
    unittest.main()
