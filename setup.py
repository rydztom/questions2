import os
import nose
from setuptools.command.test import test
from django.core import management
from setuptools import Command

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

os.environ['DJANGO_SETTINGS_MODULE'] = 'hellodjango.settings'

class test_(test):

    def run(self):
        delete_base_file()
        management.call_command('syncdb', interactive=False)
        #management.call_command('loaddata', 'fixtures.json', interactive=False)
        test.run(self)

def delete_base_file():
    filename = os.path.dirname(__file__) + 'test_db.sqlite3'
    try:
        os.remove(filename)
    except OSError:
        pass

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().split('\n')

config = {
    'name': 'questions2',
    'version': '1.0.0',
    'url': 'http://questions2.heroku.com',
    'test_suite': 'nose.collector',
    'author': 'Tomasz Rydz',
    'author_email': 'rydz.tom@gmail.com',
    'dependency_links': read('requirements.txt'),
    'license': 'BSD',
    'cmdclass': {
        'test': test_
    }
}

setup(**config)