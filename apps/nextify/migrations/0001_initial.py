# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        #('acl', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('acronym', models.CharField(unique=True, max_length=5)),
                ('name', models.CharField(unique=True, blank=True, max_length=50)),
                ('name_en', models.CharField(unique=True, blank=True, max_length=50)),
                ('id', models.AutoField(db_column='id',serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
                'db_table': 'sarv_database',
            },
        ),
        migrations.CreateModel(
            name='SarvCustomDataset',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=50)),
                ('params', models.TextField()),
                ('id', models.AutoField(db_column='id',serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
                'db_table': 'sarv_custom_datasets',
            },
        ),
        migrations.CreateModel(
            name='SarvMenu',
            fields=[
                ('id', models.AutoField(db_column='id',auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('column', models.IntegerField(null=True, blank=True)),
                ('row', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'sarv_menu',
                'ordering': ('column', 'row'),
            },
        ),
        migrations.CreateModel(
            name='SarvPage',
            fields=[
                ('id', models.AutoField(db_column='id',auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('url', models.CharField(null=True, blank=True, max_length=400)),
                ('language', models.CharField(max_length=6)),
                ('visibility', models.CharField(choices=[('public', 'public'), ('users', 'users'), ('acl', 'acl')], max_length=10)),
                ('settings', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'sarv_page',
            },
        ),
        migrations.CreateModel(
            name='SarvSession',
            fields=[
                ('id', models.AutoField(db_column='id',auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('user', models.CharField(max_length=30)),
                ('active', models.IntegerField()),
                ('session_start', models.DateTimeField()),
                ('session_end', models.DateTimeField(blank=True,null=True)),
                ('database_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'sarv_session',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(unique=True, verbose_name='Kasutajanimi', max_length=10)),
                #('agent', models.ForeignKey("Agent", null=False, blank=False, db_column='agent_id', verbose_name='Isik')),
                ('forename', models.CharField(verbose_name='Eesnimi', blank=True, max_length=50)),
                ('surename', models.CharField(verbose_name='Perekonnanimi', blank=True, max_length=50)),
                ('email', models.CharField(verbose_name='E-post', blank=True, max_length=100)),
                ('remarks', models.TextField(verbose_name='Lisainfo', blank=True)),
                ('isikukood', models.BigIntegerField(null=True, verbose_name='Eesti isikukood', blank=True)),
                ('priv', models.IntegerField(null=True, verbose_name='Privileegid', blank=True)),
                ('dbs', models.CharField(verbose_name='Andmebaasid', blank=True, max_length=50)),
                ('db', models.CharField(verbose_name='Andmebaas (tekstina)', blank=True, max_length=20)),
                ('user_added', models.CharField(verbose_name='Sisestaja', blank=True, max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Sisestatud', null=True)),
                ('user_changed', models.CharField(verbose_name='Muutja', blank=True, max_length=10)),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='Muudetud', null=True)),
                ('id', models.AutoField(db_column='id',auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('database', models.ForeignKey(db_column='database_id', editable=True, blank=True, null=True, verbose_name='Andmebaas', to='nextify.Database')),
            ],
            options={
                'db_table': 'user',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='SarvIssueType',
            fields=[
                ('issue_type', models.CharField(max_length=25)),
                ('user_created', models.ForeignKey(to='nextify.User', editable=False, null=True, blank=True, db_column='user_created_id', related_name='user1')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)),
                ('user_modified', models.ForeignKey(to='nextify.User', editable=False, null=True, blank=True, db_column='user_modified_id', related_name='user2')),
                ('timestamp_modified', models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)),
                ('id', models.AutoField(primary_key=True, db_column='id'))
            ],
            options={
                'db_table': 'sarv_issue_type'
            }
        ),
        migrations.CreateModel(
            name='SarvIssue',
            fields=[
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('response', models.TextField()),
                ('url', models.TextField()),
                ('issue_type', models.ForeignKey(to='nextify.SarvIssueType', null=True, blank=True, db_column='issue_type', verbose_name='Probleemi tüüp')),
                ('reported_by', models.ForeignKey(to='nextify.User', null=True, blank=True, db_column='reported_by', verbose_name='Sisestaja')),
                ('reported_to', models.ForeignKey(to='nextify.User', null=True, blank=True, db_column='reported_to', verbose_name='Suunatud')),
                ('database', models.ForeignKey(to='nextify.Database', editable=False, db_column='database_id', verbose_name='Andmebaas')),
                ('resolved', models.BooleanField()),
                ('id', models.AutoField(primary_key=True, db_column='id')),
                ('user_added', models.CharField(max_length=10, blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, blank=True)),
                ('user_changed', models.CharField(max_length=10, blank=True)),
                ('date_changed', models.DateTimeField(auto_now=True, null=True, blank=True))
            ],
            options={
                'db_table': 'sarv_issue'
            },
        ),
        migrations.AddField(
            model_name='sarvmenu',
            name='page',
            field=models.ForeignKey(null=True, blank=True, to='nextify.SarvPage'),
        )#,
        #migrations.AddField(
        #    model_name='sarvmenu',
        #    name='usergroup',
        #    field=models.ForeignKey(null=True, blank=True, to='acl.AclUserGroup'),
        #),
    ]
