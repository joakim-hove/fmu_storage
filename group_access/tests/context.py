import getpass
import os
import grp

class TestContext(object):

    def __init__(self):
        self.user = getpass.getuser()
        self.group = grp.getgrgid( os.getgid( ) )[0]
