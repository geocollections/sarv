from django import template
from django.db.models import Q
from sarv.utils import get_model
Menu = get_model("SarvMenu")

register = template.Library()

def main_menu(context):
    # context - dict, with {sarvuser:<User:User object>,'database':'git'}
    allowed_urls = []
    if context['acl']:
        allowed_urls = [url.replace('+','/') \
                        for url in context['acl'].keys() \
                        if context['acl'][url][0] is True]
    menu = Menu.objects \
            .filter(Q(page__url__in=allowed_urls)|Q(row=0)) \
            .order_by('column','row')
    output={}
    for v in menu:
        if v.column not in output:
            output.update({v.column:[]})
        if v.page \
        and v.page.url \
        and v.page.url[-4:] == '.php' \
        and not v.page.url.startswith('sarv_php'):
            v.page.url = 'sarv_php/%s' % v.page.url.replace('sarv_intra/','')
        output[v.column].append(v)
    outp={}
    for k in output.keys():
        if len(output[k]) > 1:
            outp[k] = output[k]

    return {'content':outp}

register.inclusion_tag('menu/menu-tag.html',takes_context=True)(main_menu)
