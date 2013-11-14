.. image:: https://secure.travis-ci.org/collective/collective.portlet.usertrack.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.portlet.usertrack

Introduction
============

The user track portlet shows users that are currently active in your Plone
site. It uses the plone.validatehook to get information from the Zope
webserver.

You can configure the users shown in the portlet using several options:

timeout
  This option determines how long the system will wait before it considers
  a user to no longer be active.

roles
  With this option you can filter the users shown based on their roles.
  You can use this to only show editors for example.

folder_type
  This option influences how the role check is done. If you select a content
  type here the system will walk up through the breadcrumb trail and look for
  the first item of a selected type. The roles of the user at that location
  will be used when applying the roles check.


Caveats
=======

* The default configuration uses a global dictionary through DictStorage 
  for storing userinformation.
  This will not work with multiple ZEO clients in separate processes that
  don't share this dictionary. To use the usertrack portlet with a ZEO setup,
  install memcached and use the "MemcacheStorage" by using the following zcml
  snippet in an overrides.zcml somewhere::

      <utility
        factory="collective.portlet.usertrack.storage.MemcacheStorage"
        provides="collective.portlet.usertrack.interfaces.ITrackerStorage"
        />
