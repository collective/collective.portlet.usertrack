from Acquisition import aq_parent
from AccessControl.User import SpecialUser
from time import time
from zope.interface import Interface
from zope.component import adapter, getUtility
from plone.validatehook.interfaces import IPostValidationEvent

from collective.portlet.usertrack.interfaces import ITrackerStorage

_users = {}

@adapter(Interface, IPostValidationEvent)
def ValidateHook(object, event):
    # Skip special users like the anonymous user and the emergency user.
    if isinstance(event.user, SpecialUser):
        return

    if getattr(object, "getPhysicalPath", None) is None:
        if getattr(aq_parent(object), "getPhysicalPath", None) is not None:
            object=aq_parent(object)
        else:
            # We may be dealing with a view
            return

    userid=event.user.getId()
    user=("/".join(event.user.getPhysicalPath()[:-1]), userid)
    path="/".join(object.getPhysicalPath())
    if not path.endswith("/"):
        path+="/"

    storage = getUtility(ITrackerStorage)

    storage.storeUser(user, userid, path, time())



def GetUsersForPath(path, after=None):
    if not path.endswith("/"):
        path+="/"

    if after is None:
        return [user for (id, user) in _users.items()
                    if path.startswith(id[0])]
    else:
        return [user for (id, user) in _users.items()
                    if path.startswith(id[0]) and user['time']>=after]



