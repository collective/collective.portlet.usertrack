# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.1.2.dev0'
long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='collective.portlet.usertrack',
      version=version,
      description="User activity portlet",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone :: 4.1',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='user tracking plone',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='http://pypi.python.org/pypi/collective.portlet.usertrack',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.validatehook',
      ],
      )
