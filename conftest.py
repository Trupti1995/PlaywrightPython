import pytest
import shutil
import os

# Define the directories to be cleared
CACHE_DIRECTORIES = ['./utils/__pycache__/', '.pytest_cache', 'allure-results']

def clear_cache():
    """ Function to clear the specified cache directories. """
    for cache_dir in CACHE_DIRECTORIES:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"Cache directory {cache_dir} cleared.")
        os.makedirs(cache_dir, exist_ok=True)
        print(f"Cache directory {cache_dir} created.")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """ Hook to run before the entire test session starts. """
    clear_cache()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """ Hook to run before each test. """
    clear_cache()
