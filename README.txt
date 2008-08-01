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

* User tracking does not work in sites which use multiple ZEO clients. The
  list of active users is only kept in the memoery of the ZEO client
  processing the request, so other clients will not see any activity.
 
