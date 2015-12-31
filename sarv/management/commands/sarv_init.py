from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from apps.nextify.models import Database, User, SarvMenu, SarvPage
from apps.acl.models import Acl, AclDestination, AclGroup, AclPermissionType, AclRightsGroup, AclRightsGroupPermissionType, AclUserGroup


class Command(BaseCommand):
    help = 'Loads data into database. Creates admin user and first menu items.'

    def add_arguments(self, parser):
        parser.add_argument('--database', type=str, help = 'Database name')
        parser.add_argument('--username', type=str, help = "Default admin username. Required.")
        parser.add_argument('--personal_code', type=str, help = "Default personal code id number")

    def handle(self, *args, **options):
        if not hasattr(settings, "LANGUAGE_CODE"):
            print("No LANGUAGE_CODE specified in settings.py. Aborting")
            return;
        # create user with admin rights
        database=Database.objects.filter(acronym=options['database'][:3])
        if len(database)<1:
            database = Database(name=options['database'],acronym=options['database'][:3])
            database.save()
        else:
            database = database[0]
        username = options['username']
        personal_code = options['personal_code'] 
        new_user = User(username=username, isikukood=int(personal_code), user_added=username, db=database.acronym)
        try:
            new_user.save()
            User.objects.filter(pk=new_user.pk).update(database_id = database.pk)
            user = User.objects.get(pk=new_user.pk)
        except Exception as e:
            print(e)
            print("Aborting")
            return
        print("Admin user created")

        # Fill ACL tables 
        # sarv_acl_destination (AclDestination): remains empty
        # sarv_acl_group: [{keyword: <db.acronym> name: <db.name>}]
        aclgroup = AclGroup(keyword=database.acronym,name=database.name)
        aclgroup.save()
        print("table sarv_acl_group filled")
        #sarv_acl_permission_type: [{type_name:"read"}, {type_name:"create"}, {type_name:"update"}, {type_name:"delete"}]
        AclPermissionType.objects.bulk_create([
            AclPermissionType(type_name="read"),
            AclPermissionType(type_name="create"),
            AclPermissionType(type_name="update"),
            AclPermissionType(type_name="delete")
        ])
        print("table sarv_acl_permission_type filled")
        #sarv_acl_rights_group AclRightsGroup: [{id:1,name:"guest"},{"viewer"},{"user"},{"editor"},{id:5,name:"admin"}]
        AclRightsGroup.objects.bulk_create([
            AclRightsGroup(name="guest"),
            AclRightsGroup(name="viewer"),
            AclRightsGroup(name="user"),
            AclRightsGroup(name="editor"),
            AclRightsGroup(name="admin"),
        ])
        print("table sarv_acl_permission_group filled")
        #sarv_acl_rights_group_permission_type AclRightsGroupPermissionType: NULL
        #sarv_acl_user_group AclUserGroup: [{id:1,id_user:<admin_user_id>,id_group:<sarv_acl_group's see ainuke kirje, mis database'ga tuli>}]
        aclusergroup = AclUserGroup(user=user, group=AclGroup.objects.get(pk=aclgroup.pk))
        aclusergroup.save()
        print("table sarv_acl_user_group filled")
        admin_group=AclUserGroup.objects.get(pk=aclusergroup.pk)
        
        # create initial admin page layout
        label = SarvPage(name="Administration", url="", language=settings.LANGUAGE_CODE, visibility="acl")
        label.save()
        admin_pages = SarvPage(name="Pages administration", url="admin/menu", language=settings.LANGUAGE_CODE, visibility="acl")
        admin_pages.save()
        print("Page admin page link created")
        admin_users = SarvPage(name="User right administration", url="admin/acl", language=settings.LANGUAGE_CODE, visibility="acl")
        admin_users.save()
        print("Use right admin page link created")
        menu_label = SarvMenu(page=label, column=1, row=0, usergroup=admin_group)
        menu_label.save()
        menu_pages = SarvMenu(page=admin_pages, column=1, row=1, usergroup=admin_group)
        menu_pages.save()
        print("Page button created")
        menu_users = SarvMenu(page=admin_users, column=1, row=2, usergroup=admin_group)
        menu_users.save()
        print("Use right button created")


        # give rights to user to see these pages
        content_type=ContentType.objects.get(app_label="nextify", model="sarvpage")
        permission=AclPermissionType.objects.get(type_name="read")
        rights_group=AclRightsGroup.objects.get(name="admin")
        acl_label=Acl(id_tested=new_user.pk, type="group", content_type=content_type, object_id=label.pk, permission=permission, rights_group=rights_group)
        acl_label.save()
        acl_pages=Acl(id_tested=new_user.pk, type="group", content_type=content_type, object_id=admin_pages.pk, permission=permission, rights_group=rights_group)
        acl_pages.save()
        acl_menu=Acl(id_tested=new_user.pk, type="group", content_type=content_type, object_id=admin_users.pk, permission=permission, rights_group=rights_group)
        acl_menu.save()
        print("acl rights created")
        print("Finished succesfully")
