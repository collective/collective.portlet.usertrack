from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.portlet.usertrack',
      version=version,
      description="User activity portlet",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='user tracking plone',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='http://plone.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.validatehook',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
