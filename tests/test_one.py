import pytest
from tornado import gen, web
from tornado.ioloop import IOLoop
from motor import MotorClient, MotorCollection
from schematics.models import Model

from tornadoMotorAcl.models import Resource, Group, Permission
from tornadoMotorAcl.validate import acl_authorize
from tornado.testing import gen_test
class MainHandler(web.RequestHandler):
    settings = None
    @property
    def db(self):
        return self.settings['db']

    @property
    def current_user(self):
        return self.settings['current_user']

    @gen.coroutine
    @acl_authorize(("read","egen stamdata"))
    def post(self):
        self.write("ok")

class TestOne:
    def setup(self):
        print "-setup"
        self.io_loop = IOLoop.instance()
        self.client = MotorClient()
        self.db = self.client.test_database

    def teardown(self):
        self.db = None
        self.client.drop_database('test_database')

    @gen_test
    def test_setup(self):

        collection = MotorCollection(self.db, 'test_collection')
        assert collection.name == 'test_collection'
        yield collection.insert({"_id":1})
        doc = yield collection.find_one({"_id":1})
        print doc, type(doc)
        assert doc['_id'] == 1

