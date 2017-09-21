import grp

class GroupAccess(object):

    def __init__(self):
        self.groups = {}


    def add_group(self,group):
        try:
            group_entry = grp.getgrnam( group )
            self.groups[ group ] = set( group_entry.gr_mem )
        except KeyError:
            pass


    def access(self, group, user):
        if not group in self.groups:
            self.add_group( group )

        if not group in self.groups:
            return False

        return user in self.groups[group]


    def __call__(self, group, user):
        return self.access( group, user )
