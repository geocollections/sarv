"""
Default Django models for Sarv project. 
Additionally ACL app has its own models.py file.
"""
from django.db import models

class Database(models.Model):
    acronym = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50, unique=True, blank=True)
    name_en = models.CharField(max_length=50, unique=True, blank=True)
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    class Meta:
        db_table = "database"
    def __unicode__(self):
        return self.acronym

# User is able to create custom filtersets for pages
class SarvCustomDataset(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    user = models.CharField(max_length=50,null=False,blank=False)
    params = models.TextField(blank=False)
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    class Meta:
        db_table = 'sarv_custom_datasets'

# Menu organization.
# Different user groups could have different layouts of menu items
class SarvMenu(models.Model):
    column = models.IntegerField(max_length=2, null=True, blank=True)
    row = models.IntegerField(max_length=2, null=True, blank=True)
    page = models.ForeignKey("SarvPage", null=True,blank=True)
    usergroup = models.ForeignKey("acl.AclUserGroup", null=True,blank=True)
    class Meta:
        db_table = 'sarv_menu'
        ordering = ('column','row')

# Page items used in menu as well as controlling the
# availability of page urls
class SarvPage(models.Model):
    VISIBILITY_CHOICES = (('public','public'),('users','users'),('acl','acl'))
    name = models.CharField(max_length=400, blank=False, null=False)
    url = models.CharField(max_length=400, blank=True, null=True)
    language = models.CharField(max_length=3,blank=False, null=False)
    visibility = models.CharField(max_length=10,choices=VISIBILITY_CHOICES)
    settings = models.TextField(blank=True,null=True)
    class Meta:
        db_table = 'sarv_page'

# Keeping track of logged in users
class SarvSession(models.Model):
    user = models.CharField(max_length=30)
    active = models.IntegerField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    database_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'sarv_session'

# User table used in authentication (ID-card)
class User(models.Model):
    session_db = None
    username = models.CharField(max_length=10, unique=True, verbose_name='Kasutajanimi')
    #agent = models.ForeignKey(Agent, null=False, blank=False, db_column='agent_id', verbose_name='Isik')
    forename = models.CharField(max_length=50, blank=True, verbose_name='Eesnimi')
    surename = models.CharField(max_length=50, blank=True, verbose_name='Perekonnanimi')
    #title = models.CharField(max_length=20, blank=True, verbose_name='Sisestatud')
    #profession = models.CharField(max_length=50, blank=True, verbose_name='Sisestatud')
    #institution_name = models.CharField(max_length=255, blank=True, verbose_name='Sisestatud')
    #phone = models.CharField(max_length=20, blank=True, verbose_name='Sisestatud')
    email = models.CharField(max_length=100, blank=True, verbose_name='E-post')
    remarks = models.TextField(blank=True, verbose_name='Lisainfo')
    isikukood = models.IntegerField(null=True, blank=True, verbose_name='Eesti isikukood')
    priv = models.IntegerField(null=True, blank=True, verbose_name='Privileegid')
    dbs = models.CharField(max_length=50, blank=True, verbose_name='Andmebaasid')
    db = models.CharField(max_length=20, blank=True, verbose_name='Andmebaas (tekstina)')
    database = models.ForeignKey(Database, editable=False, db_column='database_id', verbose_name='Andmebaas')
    user_added = models.CharField(max_length=10, blank=True, verbose_name='Sisestaja')
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Sisestatud')
    user_changed = models.CharField(max_length=10, blank=True, verbose_name='Muutja')
    date_changed = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Muudetud')
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    #objects = FilterByDbManager()
    class Meta:
        db_table = 'user'
        ordering = ['username']
    def save(self, *args, **kwargs):
        self.database_id=self.session_db
        super(User, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.username)
    def __unicode__(self):
        return str(self.username)
