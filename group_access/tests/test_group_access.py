import unittest
from group_access import GroupAccess

from context import TestContext

class GroupAccessTest(unittest.TestCase):

    def setUp(self):
        self.context = TestContext( )


    def test_create(self):
        gac = GroupAccess( )
        self.assertFalse( gac.access("group_does_not_exist", "user_does_not_exist") )
        self.assertFalse( gac.access("group_does_not_exist" , self.context.user ))
        self.assertFalse( gac.access(self.context.group, "user_does_not_exist" ))
        self.assertTrue( gac.access(self.context.group, self.context.user ))

        self.assertFalse( gac("group_does_not_exist", "user_does_not_exist") )
        self.assertFalse( gac("group_does_not_exist" , self.context.user ))
        self.assertFalse( gac(self.context.group, "user_does_not_exist" ))
        self.assertTrue( gac(self.context.group, self.context.user ))
