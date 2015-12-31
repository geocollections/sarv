from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.conf import settings

#
class Acl(models.Model):
    USER_TYPE = (("user", "user"),("group", "group"))
    id_tested = models.PositiveIntegerField()
    type = models.CharField(choices=USER_TYPE, max_length=50)
    destination = models.ForeignKey("AclDestination", db_column="id_destination", blank=True, null=True)
    
    content_type = models.ForeignKey(ContentType, db_column="destination_type", null=True, blank=True)
    object_id = models.PositiveIntegerField(db_column="id_destination_row")
    destination_object = generic.GenericForeignKey("content_type","object_id")
    
    permission = models.ForeignKey("AclPermissionType", db_column="id_permission", blank=True, null=True)
    
    rights_group = models.ForeignKey("AclRightsGroup", blank=True, null=True)
    class Meta:
        db_table = "sarv_acl"
        app_label = "acl"
#
class AclDestination(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    keyword = models.CharField(max_length=50, blank=False, null=True)
    model = models.CharField(max_length=50, blank=False, null=True)
    id_ct = models.PositiveIntegerField(db_column="id_ct")
    class Meta:
        db_table = "sarv_acl_destination"
        app_label = "acl"
#
class AclGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    keyword = models.CharField(max_length=20, blank=False)
    name = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = "sarv_acl_group"
        app_label = "acl"
#        
class AclPermissionType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    type_name = models.CharField(max_length=50, blank=True, null=False)
    class Meta:
        db_table = "sarv_acl_permission_type"
        app_label = "acl"
#
class AclRightsGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    name = models.CharField(max_length=20, blank=False, null=False)
    rights = models.ManyToManyField(AclPermissionType, through="AclRightsGroupPermissionType")
    class Meta:
        db_table = "sarv_acl_rights_group"
        app_label = "acl"
#        
class AclRightsGroupPermissionType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    SCOPE = (("False", False),("own", "own"),("True", True))
    group = models.ForeignKey(AclRightsGroup, db_column="rights_group_id")
    permission_type = models.ForeignKey(AclPermissionType, db_column="permission_type_id")
    scope = models.CharField(choices=SCOPE, max_length=10)
    class Meta:
        db_table = "sarv_acl_rights_group_permission_type"
        app_label = "acl"
#!
class AclUserGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    user = models.ForeignKey("%s.User" % settings.MODEL_APP.replace("apps.",""), db_column="id_user", null=True, blank=True)
    group = models.ForeignKey("AclGroup", db_column="id_group", null=True, blank=True)
    class Meta:
        db_table = "sarv_acl_user_group"
        app_label = "acl"
