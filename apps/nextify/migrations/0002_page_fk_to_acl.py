# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0001_initial'),
        ('nextify', '0001_initial')
    ]

    operations = [
        migrations.AddField(
            model_name='sarvmenu',
            name='usergroup',
            field=models.ForeignKey(null=True, blank=True, to='acl.AclUserGroup'),
        )
    ]
