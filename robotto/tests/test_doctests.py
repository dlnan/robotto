import os
import unittest
import doctest
from functools import partial

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class DoctestCase(unittest.TestCase):
    def __new__(self, test):
        return getattr(self, test)()

    @classmethod
    def test_docs(cls):
        import manuel.testing
        import manuel.codeblock
        import manuel.doctest
        import manuel.capture
        m = manuel.doctest.Manuel()
        m += manuel.codeblock.Manuel()
        m += manuel.capture.Manuel()

        import pkg_resources
        filename = partial(pkg_resources.resource_filename, "robotto")

        path = filename("docs")
        docs = [os.path.join(path, filename)
                for filename in os.listdir(path)]

        return manuel.testing.TestSuite(m, *docs)
