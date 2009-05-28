from zope.interface import implements
import os

from collective.portlet.usertrack.interfaces import ITrackerStorage

class DictStorage(object):
    """ a simple dict-based storage. Uses a global (module) dict,
        will not work (as expected) with ZEO setups """

    implements(ITrackerStorage)

    _users = {}

    def storeUser(self, handle, userid, path, time):
        self._users[handle] = dict(userid=userid, path=path, time=time)

    def getUser(self, path, after):
        if not path.endswith("/"):
            path+="/"

        if after is None:
            return [user for (id, user) in self._users.items()
                        if path.startswith(id[0])]
        else:
            return [user for (id, user) in self._users.items()
                        if path.startswith(id[0]) and user['time']>=after]

class MemcacheStorage(object):
    """ memcache based storage. Works with ZEO setups. Eventhough memcached
        behaves like a dictionary, we store data differently because it's
        more efficient with lookups. We want to avoid iterating over all
        items in memcached """

    implements(ITrackerStorage)

    namespace = "collective.portlet.usertrack"

    ## memcache timeouts
    ## evt opslaan per sub-path
    ## memcache host/port via env

    def getMCClient(self):
        import memcache

        if hasattr(self, 'cache'):
            return self.cache

        mchostport = os.environ.get('MEMCACHE_HOST', '127.0.0.1:11211')
        if ':' in mchostport:
            host, port = mchostport.split(':', 1)
            try:
                port = int(port)
            except ValueError, e:
                port = 11211
        else:
            host = mchostport
            port = 11211

        connectstr = "%s:%d" % (host, port)
        mc = memcache.Client([connectstr], debug=0)
        self.cache = mc
        return self.cache

    def get_storage(self):
        mc = self.getMCClient()
        namespace = mc.get(self.namespace)
        if namespace is None:
            return {}
        return namespace

    def save(self, key, val):
        mc = self.getMCClient()
        storage = self.get_storage()
        storage[key] = val
        mc.set(self.namespace, storage)
        
    def storeUser(self, handle, userid, path, time):
        storage = self.get_storage()

        base, id = handle

        base_storage = storage.get(base, {})

        base_storage[id] = dict(userid=userid, path=path, time=time)

        ## cleanup?
        self.save(base, base_storage)

    def getUser(self, path, after):
        mc = self.getMCClient()

        all_bases = self.get_storage()

        res = []
        for basepath, users in all_bases.items():
            if path.startswith(basepath):
                if after is None:
                    res += users.values()
                else:
                    res += [u for u in users.values() if u['time'] >= after]
        ## cleanup?
        return res

