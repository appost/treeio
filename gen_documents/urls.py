# This file is part of Treeio.
# Created by appost

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.gen_documents.views',
        # Orders
        url(r'^order/invoice/(?P<order_id>\d+)(\.(?P<response_format>\w+))?/?$', 
            'order_invoice_view_gd', name='sales_order_invoice_view_gd'),

)
