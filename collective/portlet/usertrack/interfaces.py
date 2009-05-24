from zope.interface import Interface

class ITrackerStorage(Interface):
    """ utilities that provide storage for tracker data """

    def storeUser(handle, userid, path, time):
        """ store userdata based on a (path, userid) handle """

    def getUser(path, after=None):
        """ get a user based on path and optional 'after' timeout """
