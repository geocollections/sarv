# -*- coding: utf-8 -*-
from apps.acl.models import Acl as mAcl, AclDestination, AclGroup, AclRightsGroup, AclUserGroup
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from sarv.local_settings import ACL_USERRIGHTS
from sarv.utils import get_model
User, Menu, Page = get_model(["User", "SarvMenu", "SarvPage"])

class Acl(object):
    
    def __init__(self, **kwargs):
        pass
    
    def get_all_user_rights (self, request):
        output = {}
        uid = request.session["sarvuser_id"]
        u_gs = AclUserGroup.objects.filter(user_id=uid)
        ct = ContentType.objects.get_for_model(Page)   

        qs = mAcl.objects.filter(Q(id_tested__in=u_gs) & Q(type="group") & Q(content_type=ct)) \
                .order_by("object_id") 

        pages = {item.pk:item.url.replace("[generic]","").replace("[extify]","") \
                 for item in Page.objects.all() if item.url is not None \
                    and not len(item.url) < 1 and item.visibility == "acl"}
        ri = {} 
        for item in qs:
            rights = ACL_USERRIGHTS[int(item.rights_group_id)-1]
            ri.update({item.object_id:rights})

        for key,item in pages.items():
            rights = ri[key] if key in ri else [False]
            item = item.replace("/","+") if "admin/" in item else item
            output.update({item:rights})
        
        return output
        
    def get_page_user_rights (self, request):
        if not "acl" in request.session or\
            not self.get_page_from_url(request) in request.session["acl"]:
            return [False,False,False,False]
        return request.session["acl"][self.get_page_from_url(request)]

    def get_page_from_url (self, request):
        # @TODO: Not recognized: links to other urls i.e. https://geokogud.info:8000
        page = request.path.split("/")[1 if request.path[:1] == "/" else 0]
        if page in ["sarv_php"]:
            return request.path.split("/")[2 if request.path[:1] == "/" else 1]
        if page in ["admin"]:
            return "+".join(request.path.split("/")[1 if request.path[:1] == "/" else 0:\
                                                    3 if request.path[:1] == "/" else 2]) 
        return page

    def get_all_rights_by_user (self, given = {}):
        #if page then get rights for that page
        page = given["page"] if "page" in given else False
        ct = ContentType.objects.get_for_model(Page)
        args={"content_type":ct}
        if not page == False:
            args.update({"object_id": Page.objects.get(name=page).pk})
        rights= {}
        idt = []
        macl=mAcl.objects.filter(**args)
        for item in macl:
            if not item.type in rights:
                rights.update({item.type:{}})
            if not item.id_tested in rights[item.type]:
                rights[item.type].update({item.id_tested:{}})
            rights[item.type][item.id_tested].update({ item.object_id: item.rights_group.name })
            if item.type == "group" and not item.id_tested in idt:
                idt.append(item.id_tested)
        uidt = AclUserGroup.objects.filter(id__in=idt)
        users_qs = User.objects.filter(pk__in=[uitem.user_id for uitem in uidt])
        users = {item.pk:item.username for item in users_qs}
        for item in uidt:
            if item.user_id in users: 
                item.username = users[item.user_id]
        rights = rights["group"] if "group" in rights else {}
        output = {}
        ugrs = {item.pk:{"user":item.user.username,"group":item.group.keyword} for item in uidt}
        for key,item in rights.items():
            if not key in ugrs: 
                continue
            if not ugrs[key]["user"] in output:
                output.update({ugrs[key]["user"]:{}})
            if not ugrs[key]["group"] in output[ugrs[key]["user"]]:
                output[ugrs[key]["user"]].update({ugrs[key]["group"]:{}})
            if key in rights:
                output[ugrs[key]["user"]][ugrs[key]["group"]] = rights[key]   
        return output
                  
    def insert_page_user_right (self, given):
        """
        given={destination,group,id,permission,userlevel}
        """
        if not "destination" in given: return False
        actor_type = "group" if "group" in given else "user"
                
        if not given["destination"][0].isupper():
            try: given["destination"] = AclDestination.objects.get(keyword=given["destination"]).model
            except AclDestination.DoesNotExist: return False
        if actor_type == "group":
            try: actor_qs = AclUserGroup.objects.get(group__keyword=given["group"],user__username=given["user"])
            except AclUserGroup.DoesNotExist:
                new_group = AclUserGroup(**{
                                "group":AclGroup.objects.get(keyword=given["group"]),
                                "user":User.objects.get(username=given["user"])})
                new_group.save()
                actor_qs = new_group
        else:
            try: actor_qs = User.objects.get(username=given["user"])
            except User.DoesNotExist: return False
        dest_model = Menu if given["destination"] == "Menu" else \
                    get_model(given["destination"])
        arguments = {
                     "id_tested": actor_qs.pk,
                     "type": actor_type,
                     "content_type": ContentType.objects.get_for_model(dest_model),
                     }
        if not "save_all" in given: arguments.update({"object_id":given["id"]})
        self.remove_page_user_right(arguments)
        arguments.update({
                          "permission_id": 1,
                          "rights_group":AclRightsGroup.objects.get(name="%s"% given["userlevel"] \
                                                                    if "userlevel" in given else 1),
                          })
        if "save_all" in given:
            new_items = []
            for item in dest_model.objects.all():
                arguments.update({"object_id":item.pk})
                new_items.append(mAcl(**arguments))
            mAcl.objects.bulk_create(new_items)
        else:
            new_item = mAcl(**arguments)
            new_item.save()
        return False
    
    def remove_page_user_right (self, given):
        qs = mAcl.objects.filter(**given)
        if qs.count() > 0: qs.delete()
        
    def set_page_visibility (self, given):
        if not "id" in given: return False
        page_id = given["id"]
        
