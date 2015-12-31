# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0001_initial'),
        #('contenttypes', '0001_initital'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('nextify', '0002_page_fk_to_acl')
    ]

    operations = [
        migrations.AddField(
            model_name='acl',
            name='content_type', 
            field=models.ForeignKey(db_column='destination_type', to='contenttypes.ContentType'))
    ]
