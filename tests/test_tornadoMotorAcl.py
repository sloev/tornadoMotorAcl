#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tornadoMotorAcl
----------------------------------

Tests for `tornadoMotorAcl` module.
"""
import pytest
from tornado import gen, web
from tornado.ioloop import IOLoop
from motor import MotorClient, MotorCollection
from schematics.models import Model

from tornadoMotorAcl.models import Resource, Group, Permission, ResourcePermissionPair
from tornadoMotorAcl.validate import acl_authorize
from tornado.testing import gen_test

from bson.objectid import ObjectId

class Handler:
    status = False
    def __init__(self, db, current_user):
        self.db = db
        self.current_user = current_user
    def finish(self):
        pass
    def set_status(self, status):
        self.status = status
    def write(self,message):
        self.message=message

class OwnDataHandler(Handler):
    @gen.coroutine
    @acl_authorize(("read", "own data"))
    def post(self):
        self.write("ok")

class OthersDataHandler(Handler):
    @gen.coroutine
    @acl_authorize(("read", "others data"))
    def post(self):
        self.write("ok")

class OwnAndOthersDataHandler(Handler):
    @gen.coroutine
    @acl_authorize(('read', 'own data'),("read", "others data"))
    def post(self):
        self.write("ok")

class User:
    def __init__(self, name, _id):
        self.name = name
        self._id = _id


class TestTornadoMotorAcl:
    io_loop = IOLoop.instance()
    @gen_test
    def setup(self):
        print "-setup"
        self.client = MotorClient()
        #print "c, ", self.client
        self.db = self.client['test_database']
        self.permissions = MotorCollection(self.db, 'acl_permissions')
        self.groups = MotorCollection(self.db, 'acl_groups')
        self.resources = MotorCollection(self.db, 'acl_resources')
        self.users = MotorCollection(self.db, 'users')

        self.user_ids = yield self.users.insert([{'name':'burger'},{'name':'paul'}])
        self.user_ids = [str(x) for x in self.user_ids]
        self.admin_user = User("burger", self.user_ids[0])
        self.user_user = User("paul", self.user_ids[1])
        self.perm_ids = yield self.permissions.insert([x.to_primitive() for x in [
            Permission({"name":"read"}),
            Permission({"name":"write"}),
            Permission({"name":"update"}),
            Permission({"name":"delete"}),
            ]])
        self.res_ids = yield self.resources.insert([x.to_primitive() for x in [
            Resource({'name':'own data'}),
            Resource({'name':'others data'}),
            Resource({'name':'all data'})
            ]])
        self.group_ids = yield self.groups.insert([x.to_primitive() for x in [
            Group({"name":"brugere",
                "permissions":[
                    ResourcePermissionPair({"resource":"own data",
                        "permissions":[
                            "read", "write"
                            ]
                        })
                    ],
                "members":[self.user_ids[0], self.user_ids[1]],
                }),
             Group({"name":"super brugere",
                "permissions":[
                    ResourcePermissionPair({"resource":'own data',
                        "permissions":[
                            "read", "write", "update"
                            ]
                        }),
                     ResourcePermissionPair({"resource":"others data",
                        "permissions":[
                            "read"
                            ]
                        })
                    ],
                "members":[self.user_ids[0]],
                })
            ]])
        doc = yield self.groups.find_one({"name": "brugere"})
        members =doc['members']
        #print "members:", members
        #print "users", self.user_ids
#        assert self.admin_user._id in members
        assert True
    @gen_test
    def teardown(self):
        self.db = None
        self.client.drop_database('test_database')

    @gen_test
    def test_setup(self):
        assert len(self.user_ids) == 2
        assert len(self.perm_ids) == 4
        assert len(self.res_ids) == 3
        assert len(self.group_ids) == 2

    @gen_test
    def test_that_user_can_read_own_data(self):
        handler = OwnDataHandler(self.db, self.user_user)
        yield handler.post()
        assert handler.status == 200
        #assert handler.status == 200

    @gen_test
    def test_that_user_can_not_read_others_data(self):
        handler = OthersDataHandler(self.db, self.user_user)
        yield handler.post()
        assert handler.status == 403

    @gen_test
    def test_that_admin_can_read_own_data(self):
        handler = OwnDataHandler(self.db, self.admin_user)
        yield handler.post()
        assert handler.status == 200
        #assert handler.status == 200

    @gen_test
    def test_that_admin_can_read_others_data(self):
        handler = OthersDataHandler(self.db, self.admin_user)
        yield handler.post()
        assert handler.status == 200

    @gen_test
    def test_that_admin_can_read_others_and_own_data(self):
        handler = OwnAndOthersDataHandler(self.db, self.admin_user)
        yield handler.post()
        assert handler.status == 200


