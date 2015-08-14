import pytest
from tornado import gen, web
from tornado.ioloop import IOLoop
from motor import MotorClient
from schematics.models import Model

from tornadoMotorAcl.models import Resource, Group, Permission
from tornadoMotorAcl.validate import acl_authorize

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
        db = MotorClient().test
        def callback(a,b):
            print "callback", a,b
        _id = yield db["users"].insert({"name":"test"}, callback=callback)
        print _id
        print db
    def teardown(self):
        print "- teardown"
    def test_one(self):
        print "- test one"
        assert True
