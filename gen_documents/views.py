# This file is part of Treeio.
# Created by appost


from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from treeio.sales.models import Product, SaleOrder, SaleSource, Lead, Opportunity, \
                                  SaleStatus, Subscription, OrderedProduct
from treeio.sales.forms import SettingsForm, OrderForm, ProductForm, SaleStatusForm, UpdateRecordForm, \
                                 LeadForm, OpportunityForm, OrderedProductForm, SubscriptionForm, \
                                 OrderFilterForm, LeadFilterForm, OpportunityFilterForm, ProductFilterForm, \
                                 MassActionForm, ProductMassActionForm, LeadMassActionForm, \
                                 OpportunityMassActionForm, SaleSourceForm
from treeio.core.rendering import render_to_response
from treeio.core.models import Object, ModuleSetting, UpdateRecord
from treeio.core.views import user_denied
from treeio.core.decorators import treeio_login_required, handle_response_format, module_admin_required
from treeio.identities.models import Contact
from treeio.finance.models import Currency
from treeio.finance.helpers import convert
import settings
import gen_files
from django.template import Context
import re
from treeio.core.templatetags.modules import htdatetime



@treeio_login_required
@handle_response_format
def order_invoice_view_gd(request, order_id, response_format='html'):
    "Order view as Invoice"
    order = get_object_or_404(SaleOrder, pk=order_id)
    if not request.user.get_profile().has_permission(order) \
        and not request.user.get_profile().is_admin('treeio.sales'):
        return user_denied(request, message="You don't have access to this Sale")
    
    ordered_products = order.orderedproduct_set.filter(trash=False)
    
    # default company
    try:
        conf = ModuleSetting.get_for_module('treeio.finance', 'my_company')[0]
        my_company = Contact.objects.get(pk=long(conf.value))
             
    except:
        my_company = None
    fullpath = getattr(settings, 'WEBODT_TEMPLATE_PATH')
    odts_names = gen_files.list_odt_temp(fullpath)
    if request.GET and request.GET.keys()[0].encode('ascii') in odts_names:
        

        "Return url to download a file"
        
        data = ''
        data = open(fullpath + "/" + request.GET.keys()[0].encode('ascii')).read()
        #try:
        #    data = open(fullpath + str(file.content)).read()
        #except IOError:
        #    pass
        context = {}
        property_lst = []
        service_lst = []
        for ordered_product in ordered_products:
            ordered_product.tags_prod = ordered_product.product.tags.all()
            if ordered_product.product.product_type == 'good'.decode('utf8'):
                property_lst.append(ordered_product)
            if ordered_product.product.product_type == 'service'.decode('utf8'):
                service_lst.append(ordered_product)
        context['properties'] = property_lst
        context['services'] = service_lst
        context['deposit'] = service_lst[0].rate
        context['rent'] = property_lst[0].rate
        #import ipdb;ipdb.set_trace()
        order.datetime = htdatetime(RequestContext(request), order.datetime)
        context['order'] = order
        contact_values = order.client.contactvalue_set.all()
        context['client_email'] = contact_values.filter(field__field_type = 'email'.decode('utf-8'))[0]
        context['client_phone'] = contact_values.filter(field__field_type = 'phone'.decode('utf-8'))[0]
        client_details = contact_values.filter(field__field_type = 'details'.decode('utf-8'))[0]
        client_details.value = re.sub('<[^<]+?>', '', client_details.value)
        context['client_details'] = client_details
        context['lead_details'] = re.sub('<[^<]+?>', '', order.opportunity.lead.details)
        context['lead_details'] = context['lead_details'].split('\n')
        import ipdb; ipdb.set_trace()
        dcm = gen_files.gen_odt(fullpath + "/" + request.GET.keys()[0].encode('ascii'), Context(context), context_instance=RequestContext(request), file_name= "%s" % request.GET.keys()[0].encode('ascii'))
        #dcm_str = dcm.read()
        #dcm.close()
        
        #response = HttpResponse(dcm_str, content_type='application/x-download')
        #dcm['Content-Disposition'] = 'attachment; filename= "%s"' % request.GET.keys()[0].encode('ascii')
        return dcm
    return render_to_response('gen_documents/order_invoice_view_gd',
                              {'order': order,
                               'files': odts_names,
                               'ordered_products': ordered_products,
                               'my_company': my_company},
                              context_instance=RequestContext(request), response_format=response_format)


