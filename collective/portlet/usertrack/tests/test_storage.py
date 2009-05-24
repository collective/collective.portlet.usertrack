import unittest
import time

from collective.portlet.usertrack.storage import DictStorage, MemcacheStorage

class MockupMemcache(object):
    """ tries to behave like memcached """
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

class NonStaticDictStorage(DictStorage):
    def __init__(self):
        self._users = {}

class MockupMemcacheStorage(MemcacheStorage):
    def getMCClient(self):
        if not hasattr(self, 'mc'):
            self.mc = MockupMemcache()
        return self.mc

class BaseTest(unittest.TestCase):
    def test_empty(self):
        s = self.storage()
        res = s.getUser('/foo', 0)
        self.assertEquals(res, [])

    def test_simplefind(self):
        s = self.storage()
        s.storeUser(('/foo', 'john'), 'john', '/foo/bar', time.time())
        res = s.getUser('/foo', 0)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['userid'], 'john')
        self.assertEquals(res[0]['path'], '/foo/bar')

    def test_different_basepath(self):
        s = self.storage()
        s.storeUser(('/foo', 'john'), 'john', '/foo/bar', time.time())
        res = s.getUser('/bar', 0)
        self.assertEquals(res, [])

    def test_multiplepath(self):
        s = self.storage()
        s.storeUser(('/foo', 'john'), 'john', '/foo/bar', time.time())
        s.storeUser(('/foo', 'john'), 'john', '/foo/bla/somewhere', time.time())
        res = s.getUser('/foo', 0)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['userid'], 'john')
        self.assertEquals(res[0]['path'], '/foo/bla/somewhere')

    def test_multipleuser(self):
        s = self.storage()
        s.storeUser(('/foo', 'john'), 'john', '/foo/bar', time.time())
        s.storeUser(('/foo', 'peter'), 'peter', '/foo/bar', time.time())
        res = s.getUser('/foo', 0)
        self.assertEquals(len(res), 2)
        self.failUnless('john' in [u['userid'] for u in res])
        self.failUnless('peter' in [u['userid'] for u in res])

    def test_timeout(self):
        s = self.storage()
        ## 10 seconds ago
        s.storeUser(('/foo', 'john'), 'john', '/foo/bar', time.time() - 10)
        ## find not older that 5 seconds ago
        res = s.getUser('/foo', time.time() - 5)
        self.assertEquals(res, [])

    def test_notimeout(self):
        s = self.storage()
        ## 10 seconds ago
        s.storeUser(('/foo', 'john'), 'john', '/foo/bar', time.time() - 10)
        ## find not older that 15 seconds ago
        res = s.getUser('/foo', time.time() - 15)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['userid'], 'john')

class TestDictStorage(BaseTest):
    storage = NonStaticDictStorage

class TestMemcachedStorage(BaseTest):
    storage = MockupMemcacheStorage

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestDictStorage),
        unittest.makeSuite(TestMemcachedStorage),
    ))

