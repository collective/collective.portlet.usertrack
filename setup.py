from setuptools import setup, find_packages
import os

version = '1.1.2.dev0'

setup(name='collective.portlet.usertrack',
      version=version,
      description="User activity portlet",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='user tracking plone',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='http://pypi.python.org/pypi/collective.portlet.usertrack',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.validatehook',
      ],
      )
