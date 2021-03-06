import os
import sys
import unittest


# Ensure that the torch directory is part of our Python path.
APP_ROOT = os.path.realpath(os.path.dirname(__file__) + '/../')
sys.path.append(APP_ROOT)

# Configure empty settings.
from django.conf import settings
settings.configure()

# Find tests.
def load_tests(loader, standard_tests, throwaway):
    return loader.discover('tests')

# Run the tests.
if __name__ == '__main__':
    unittest.main()
