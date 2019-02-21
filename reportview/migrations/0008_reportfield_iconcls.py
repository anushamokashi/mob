# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-25 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportview', '0007_auto_20180718_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportfield',
            name='iconcls',
            field=models.CharField(blank=True, choices=[(b'add', b'Add'), (b'albums', b'Albums'), (b'logo-android', b'Android'), (b'logo-angular', b'Angular'), (b'aperture', b'Aperture'), (b'logo-apple', b'Apple'), (b'apps', b'Apps'), (b'archive', b'Archive'), (b'barcode', b'Barcode'), (b'basket', b'Basket'), (b'bicycle', b'Bicycle'), (b'logo-bitcoin', b'Bitcoin'), (b'bonfire', b'Bonefire'), (b'book', b'Book'), (b'bookmark', b'Bookmark'), (b'bookmarks', b'Bookmarks'), (b'briefcase', b'Briefcase'), (b'calculator', b'Calculator'), (b'calendar', b'Calendar'), (b'card', b'Card'), (b'cash', b'Cash'), (b'clock', b'Clock'), (b'cloud', b'Cloud'), (b'codepen', b'Codepen'), (b'construct', b'Construct'), (b'contact', b'Contact'), (b'copy', b'Copy'), (b'create', b'Create'), (b'cube', b'Cube'), (b'desktop', b'Desktop'), (b'disc', b'Disc'), (b'document', b'Document'), (b'flame', b'Flame'), (b'flower', b'Flower'), (b'floder', b'Floder'), (b'globe', b'Globe'), (b'grid', b'Grid'), (b'help-buoy', b'Help-Buoy'), (b'home', b'Home'), (b'images', b'Images'), (b'information-circle', b'Information-Circle'), (b'keypad', b'Keypad'), (b'laptop', b'Laptop'), (b'list-box', b'List-Box'), (b'lock', b'Lock')], max_length=100, null=True),
        ),
    ]
