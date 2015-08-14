#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tornadoMotorAcl
----------------------------------

Tests for `tornadoMotorAcl` module.
"""

import pytest
from tornado import gen, web
from motor import MotorClient
from schematics.models import Model

from tornadoMotorAcl.models import Resource, Group, Permission
from tornadoMotorAcl.validate import acl_authorize

class MainHandler(web.RequestHandler):
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


class estAclAuthorize:

    def setup(self):
        print "setting up\n"
        #return 
        #db = MotorClient()['test']
        #def a(a,b):
        #    self.user_id = a
        #yield db['users'].insert({"name":"test"}, callback=a)
        #print "user_id", str(user_id), "\n"


        print "setup module\n"

    def teardown(self):
        print "[!]teardown module\n"""

    def test_acl_authorize(self):
        print "acl_authorize\n"
        assert False
    """
    permissions = [
            Permission({"name":"read", "permission_id":1}),
            Permission({"name":"write", "permission_id": 2})
            ]
    resources = [
            Resource({"name":"egen stamdata", "resource_id":1}),
            Resource({"name":"andres stamdata", "resource_id":2})
            ]
    groups = [
            Group({"name":"brugere",
                "permissions":[
                    ResourcePermissionPair({"resource_id":1,
                        "permissions":[
                            1,2
                            ]
                        })
                    ],
                "members":[1,2],
                "group_id":1
                }),
             Group({"name":"super brugere",
                "permissions":[
                    ResourcePermissionPair({"resource_id":1,
                        "permissions":[
                            1,2
                            ]
                        }),
                     ResourcePermissionPair({"resource_id":2,
                        "permissions":[
                            1
                            ]
                        })
                    ],
                "members":[2],
                "group_id":2
                })
            ]

    class User(Model):
        name = StringType()
        uid = IntType()

    users = [
            User({"name": "oscar", "uid":1}),
            User({"name": "johannes", "uid":2})
            ]

    oscar = users[0]

    """
