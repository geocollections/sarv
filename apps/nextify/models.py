"""
Default Django models for Sarv project. 
Additionally ACL app has its own models.py file.
"""
from django.db import models

class FilterByDbManager(models.Manager):
    def get_queryset(self):
        if self.model.session_db is None:
            return super(FilterByDbManager, self).get_queryset()
        else:
            return super(FilterByDbManager, self).get_queryset().filter(database_id=self.model.session_db)

class Database(models.Model):
    acronym = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50, unique=True, blank=True)
    name_en = models.CharField(max_length=50, unique=True, blank=True)
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    class Meta:
        db_table = "sarv_database"
        app_label = "nextify"
    def __unicode__(self):
        return self.acronym

# User is able to create custom filtersets for pages
class SarvCustomDataset(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    user = models.CharField(max_length=50,null=False,blank=False)
    params = models.TextField(blank=False)
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    class Meta:
        db_table = "sarv_custom_datasets"
        app_label = "nextify"

class SarvIssue(models.Model):
    title = models.CharField(max_length=150, verbose_name='Pealkiri')
    description = models.TextField(verbose_name='Kirjeldus')
    response = models.TextField(verbose_name='vastus')
    url = models.TextField(verbose_name='url')
    issue_type = models.ForeignKey('SarvIssueType', null=True, blank=True, db_column='issue_type', verbose_name='Probleemi tüüp')
    reported_by = models.ForeignKey('User', null=True, blank=True, related_name='reported_by', db_column='reported_by', verbose_name='Sisestaja')
    reported_to = models.ForeignKey('User', null=True, blank=True, related_name='reported_to', db_column='reported_to', verbose_name='Suunatud')
    database = models.ForeignKey(Database, editable=False, db_column='database_id', verbose_name='Andmebaas')
    resolved = models.BooleanField(verbose_name='OK')
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    user_added = models.CharField(max_length=10, blank=True, verbose_name='Sisestaja')
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Sisestatud')
    user_changed = models.CharField(max_length=10, blank=True, verbose_name='Muutja')
    date_changed = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Muudetud')
    class Meta:
        db_table = 'sarv_issue'
        verbose_name = 'SARV probleem'
        ordering = ['-id',]
    def __unicode__(self):
        return self.title

class SarvIssueType(models.Model):
    issue_type = models.CharField(max_length=25, verbose_name='Vea tüüp')
    user_created = models.ForeignKey('User', editable=False, null=True, blank=True, db_column='user_created_id', related_name='user1', verbose_name='Sisestaja ID')
    timestamp_created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True, verbose_name='Sisestus')
    user_modified = models.ForeignKey('User', editable=False, null=True, blank=True, db_column='user_modified_id', related_name='user2', verbose_name='Muutja ID') 
    timestamp_modified = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True, verbose_name='Muudatus')
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    class Meta:
        db_table = 'sarv_issue_type'
    def __unicode__(self):
        return self.issue_type

# Menu organization.
# Different user groups could have different layouts of menu items
class SarvMenu(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    column = models.IntegerField(null=True, blank=True)
    row = models.IntegerField(null=True, blank=True)
    page = models.ForeignKey("SarvPage", null=True,blank=True)
    usergroup = models.ForeignKey("acl.AclUserGroup", null=True,blank=True)
    class Meta:
        db_table = "sarv_menu"
        app_label = "nextify"
        ordering = ('column','row')

# Page items used in menu as well as controlling the
# availability of page urls
class SarvPage(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    VISIBILITY_CHOICES = (('public','public'),('users','users'),('acl','acl'))
    name = models.CharField(max_length=400, blank=False, null=False)
    url = models.CharField(max_length=400, blank=True, null=True)
    language = models.CharField(max_length=6,blank=False, null=False)
    visibility = models.CharField(max_length=10,choices=VISIBILITY_CHOICES)
    settings = models.TextField(blank=True,null=True)
    class Meta:
        db_table = "sarv_page"
        app_label = "nextify"

# Keeping track of logged in users
class SarvSession(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', db_column='id')
    user = models.CharField(max_length=30)
    active = models.IntegerField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(blank=True,null=True)
    database_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "sarv_session"
        app_label = "nextify"

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
    isikukood = models.BigIntegerField(null=True, blank=True, verbose_name='Eesti isikukood')
    priv = models.IntegerField(null=True, blank=True, verbose_name='Privileegid')
    dbs = models.CharField(max_length=50, blank=True, verbose_name='Andmebaasid')
    db = models.CharField(max_length=20, blank=True, verbose_name='Andmebaas (tekstina)')
    database = models.ForeignKey(Database, editable=True, db_column='database_id', verbose_name='Andmebaas')
    user_added = models.CharField(max_length=10, blank=True, verbose_name='Sisestaja')
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Sisestatud')
    user_changed = models.CharField(max_length=10, blank=True, verbose_name='Muutja')
    date_changed = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Muudetud')
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='ID')
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    #objects = FilterByDbManager()
    class Meta:
        db_table = "user"
        app_label = "nextify"
        ordering = ['username']
    def save(self, *args, **kwargs):
        self.database_id=self.session_db
        super(User, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.username)
    def __unicode__(self):
        return str(self.username)
