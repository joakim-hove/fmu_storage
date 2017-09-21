from django.forms import *

class UploadForm(Form):
    smspec_file = FileField( )
    unsmry_file = FileField( )

    init_file = FileField( required = False )
    restart_file = FileField( required = False )
    grid_file = FileField( required = False )
    data_file = FileField( required = False )
    group = CharField( max_length = 32 )
