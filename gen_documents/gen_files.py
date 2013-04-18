# This file is part of Treeio.
# Created by appost

import os
import webodt
from django.template import Context
import webodt.shortcuts

def list_odt_temp(path):
    return os.listdir(path)


def gen_odt(odt_template, context, context_instance):
    #import ipdb; ipdb.set_trace()
    #template = webodt.ODFTemplate(odt_template)
    #document = template.render(Context(context))
    document = webodt.shortcuts.render_to('odt', odt_template, context, context_instance)
    return document
    
