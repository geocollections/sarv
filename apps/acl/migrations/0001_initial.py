# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        #('contenttypes', '0002_remove_content_type_name'),
        ('nextify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acl',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('id_tested', models.PositiveIntegerField()),
                ('type', models.CharField(max_length=50, choices=[('user', 'user'), ('group', 'group')])),
                ('object_id', models.PositiveIntegerField(db_column='id_destination_row')),
                #('content_type', models.ForeignKey(db_column='destination_type', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'sarv_acl',
            },
        ),
        migrations.CreateModel(
            name='AclDestination',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50, null=True)),
                ('model', models.CharField(max_length=50, null=True)),
                ('id_ct', models.PositiveIntegerField(db_column='id_ct')),
            ],
            options={
                'db_table': 'sarv_acl_destination',
            },
        ),
        migrations.CreateModel(
            name='AclGroup',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('keyword', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'db_table': 'sarv_acl_group',
            },
        ),
        migrations.CreateModel(
            name='AclPermissionType',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'db_table': 'sarv_acl_permission_type',
            },
        ),
        migrations.CreateModel(
            name='AclRightsGroup',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'sarv_acl_rights_group',
            },
        ),
        migrations.CreateModel(
            name='AclRightsGroupPermissionType',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('scope', models.CharField(max_length=10, choices=[('False', False), ('own', 'own'), ('True', True)])),
                ('group', models.ForeignKey(db_column='rights_group_id', to='acl.AclRightsGroup')),
                ('permission_type', models.ForeignKey(db_column='permission_type_id', to='acl.AclPermissionType')),
            ],
            options={
                'db_table': 'sarv_acl_rights_group_permission_type',
            },
        ),
        migrations.CreateModel(
            name='AclUserGroup',
            fields=[
                ('id', models.AutoField(db_column='id', serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('group', models.ForeignKey(to='acl.AclGroup', db_column='id_group', null=True, blank=True)),
                ('user', models.ForeignKey(to='nextify.User', db_column='id_user', null=True, blank=True)),
            ],
            options={
                'db_table': 'sarv_acl_user_group',
            },
        ),
        migrations.AddField(
            model_name='aclrightsgroup',
            name='rights',
            field=models.ManyToManyField(through='acl.AclRightsGroupPermissionType', to='acl.AclPermissionType'),
        ),
        migrations.AddField(
            model_name='acl',
            name='destination',
            field=models.ForeignKey(to='acl.AclDestination', db_column='id_destination', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='acl',
            name='permission',
            field=models.ForeignKey(to='acl.AclPermissionType', db_column='id_permission', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='acl',
            name='rights_group',
            field=models.ForeignKey(to='acl.AclRightsGroup', null=True, blank=True),
        ),
    ]
