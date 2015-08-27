import os
import sys
from setuptools import setup
from django.core import management

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

currentdir = os.getcwd()
os.chdir(os.path.join(currentdir, 'paiji2_utils'))
management.call_command('compilemessages', stdout=sys.stdout)
os.chdir(currentdir)

setup(
    name='django-paiji2-utils',
    version='0.1',
    packages=['paiji2_utils',],
    include_package_data=True,
    description='Some utils used by all paiji2 modules',
    long_description=README,
    url='https://github.com/rezometz/django-paiji2-utils',
    author='Paiji dev',
    author_email='paiji-dev@rezometz.org',
    install_requires=[
        'Django>=1.6',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
