# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-31 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0004_ionicnotification'),
        ('transactionview', '0016_auto_20180508_1809'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('sql', models.TextField()),
                ('is_main_query', models.BooleanField(default=False)),
                ('join_type', models.CharField(blank=True, choices=[(b'none', b'None'), (b'left-outer-join', b'Left Outer Join'), (b'inner-join', b'Inner Join'), (b'cross-join', b'Cross Join')], max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Query',
                'verbose_name_plural': 'Querys',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('enable_header', models.BooleanField(default=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('report_header_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('report_header_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('report_footer_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('report_footer_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('row_count', models.SmallIntegerField(default=10)),
                ('is_hidden', models.BooleanField(default=False)),
                ('report_type', models.CharField(blank=True, choices=[(b'onlinereport', b'OnlineReport'), (b'offlinereport', b'OfflineReport'), (b'displayreport', b'Displayreport')], max_length=20, null=True)),
                ('report_description', models.CharField(blank=True, max_length=2000, null=True)),
                ('lines_per_page', models.PositiveSmallIntegerField(default=0)),
                ('show_grand_total', models.BooleanField(default=False)),
                ('template_type', models.CharField(blank=True, choices=[(b'card', b'Card'), (b'list', b'List')], max_length=20, null=True)),
                ('rowtemplate', models.TextField(blank=True, null=True)),
                ('identifiers', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.CreateModel(
            name='ReportAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('report_action', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_actions', to='reportview.Report')),
            ],
            options={
                'verbose_name': 'ReportAction',
                'verbose_name_plural': 'ReportActions',
            },
        ),
        migrations.CreateModel(
            name='ReportCSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('iconcls', models.CharField(blank=True, choices=[(b'add', b'Add'), (b'albums', b'Albums'), (b'logo-android', b'Android'), (b'logo-angular', b'Angular'), (b'aperture', b'Aperture'), (b'logo-apple', b'Apple'), (b'apps', b'Apps'), (b'archive', b'Archive'), (b'barcode', b'Barcode'), (b'basket', b'Basket'), (b'bicycle', b'Bicycle'), (b'logo-bitcoin', b'Bitcoin'), (b'bonfire', b'Bonefire'), (b'book', b'Book'), (b'bookmark', b'Bookmark'), (b'bookmarks', b'Bookmarks'), (b'briefcase', b'Briefcase'), (b'calculator', b'Calculator'), (b'calendar', b'Calendar'), (b'card', b'Card'), (b'cash', b'Cash'), (b'clock', b'Clock'), (b'cloud', b'Cloud'), (b'codepen', b'Codepen'), (b'construct', b'Construct'), (b'contact', b'Contact'), (b'copy', b'Copy'), (b'create', b'Create'), (b'cube', b'Cube'), (b'desktop', b'Desktop'), (b'disc', b'Disc'), (b'document', b'Document'), (b'flame', b'Flame'), (b'flower', b'Flower'), (b'floder', b'Floder'), (b'globe', b'Globe'), (b'grid', b'Grid'), (b'help-buoy', b'Help-Buoy'), (b'home', b'Home'), (b'images', b'Images'), (b'information-circle', b'Information-Circle'), (b'keypad', b'Keypad'), (b'laptop', b'Laptop'), (b'list-box', b'List-Box'), (b'lock', b'Lock')], max_length=100, null=True)),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reportview.Report')),
                ('report_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reportview.ReportAction')),
            ],
            options={
                'verbose_name': 'ReportCSV',
                'verbose_name_plural': 'ReportCSVs',
            },
        ),
        migrations.CreateModel(
            name='ReportEpostMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ReportField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('caption', models.CharField(max_length=255, null=True)),
                ('data_type', models.CharField(blank=True, choices=[(b'char', b'Char'), (b'numeric', b'Numeric'), (b'datetime', b'DateTime'), (b'template_column', b'Template Column')], max_length=20, null=True)),
                ('no_of_decimal_digits', models.SmallIntegerField(default=0)),
                ('show_running_total', models.BooleanField(default=False)),
                ('show_total', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('apply_comma', models.BooleanField(default=False)),
                ('dont_repeat', models.BooleanField(default=False)),
                ('column_alignment', models.CharField(blank=True, choices=[(b'left', b'Left'), (b'center', b'Center'), (b'right', b'Right')], max_length=20, null=True)),
                ('dont_show_zero', models.BooleanField(default=False)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('width', models.PositiveSmallIntegerField(default=0)),
                ('height', models.PositiveSmallIntegerField(default=0)),
                ('query', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reportview.Query')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_fields', to='reportview.Report')),
            ],
            options={
                'verbose_name': 'ReportField',
                'verbose_name_plural': 'ReportFields',
            },
        ),
        migrations.CreateModel(
            name='ReportGrouping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_caption_template', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_caption_template', models.CharField(blank=True, max_length=255, null=True)),
                ('show_line_space', models.BooleanField(default=False)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('caption_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reportview.ReportField')),
                ('groupby_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reportview.ReportField')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_groupings', to='reportview.Report')),
            ],
            options={
                'verbose_name': 'ReportGrouping',
                'verbose_name_plural': 'ReportGroupings',
            },
        ),
        migrations.CreateModel(
            name='ReportHTML',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('iconcls', models.CharField(blank=True, choices=[(b'add', b'Add'), (b'albums', b'Albums'), (b'logo-android', b'Android'), (b'logo-angular', b'Angular'), (b'aperture', b'Aperture'), (b'logo-apple', b'Apple'), (b'apps', b'Apps'), (b'archive', b'Archive'), (b'barcode', b'Barcode'), (b'basket', b'Basket'), (b'bicycle', b'Bicycle'), (b'logo-bitcoin', b'Bitcoin'), (b'bonfire', b'Bonefire'), (b'book', b'Book'), (b'bookmark', b'Bookmark'), (b'bookmarks', b'Bookmarks'), (b'briefcase', b'Briefcase'), (b'calculator', b'Calculator'), (b'calendar', b'Calendar'), (b'card', b'Card'), (b'cash', b'Cash'), (b'clock', b'Clock'), (b'cloud', b'Cloud'), (b'codepen', b'Codepen'), (b'construct', b'Construct'), (b'contact', b'Contact'), (b'copy', b'Copy'), (b'create', b'Create'), (b'cube', b'Cube'), (b'desktop', b'Desktop'), (b'disc', b'Disc'), (b'document', b'Document'), (b'flame', b'Flame'), (b'flower', b'Flower'), (b'floder', b'Floder'), (b'globe', b'Globe'), (b'grid', b'Grid'), (b'help-buoy', b'Help-Buoy'), (b'home', b'Home'), (b'images', b'Images'), (b'information-circle', b'Information-Circle'), (b'keypad', b'Keypad'), (b'laptop', b'Laptop'), (b'list-box', b'List-Box'), (b'lock', b'Lock')], max_length=100, null=True)),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reportview.Report')),
                ('report_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reportview.ReportAction')),
            ],
            options={
                'verbose_name': 'ReportHTML',
                'verbose_name_plural': 'ReportHTMLs',
            },
        ),
        migrations.CreateModel(
            name='ReportParamField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('caption', models.CharField(blank=True, max_length=255, null=True)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('is_hidden', models.BooleanField(default=False)),
                ('no_of_decimal_digits', models.PositiveSmallIntegerField(default=0)),
                ('data_type', models.CharField(blank=True, choices=[(b'char', b'Char'), (b'numeric', b'Numeric'), (b'datetime', b'DateTime'), (b'template_column', b'Template Column')], max_length=20, null=True)),
                ('value_field', models.CharField(blank=True, max_length=100, null=True)),
                ('display_field', models.CharField(blank=True, max_length=100, null=True)),
                ('allow_empty', models.BooleanField(default=False)),
                ('expression', models.TextField(blank=True, null=True)),
                ('expression_postfix', models.TextField(blank=True, null=True)),
                ('validate_expression', models.TextField(blank=True, null=True)),
                ('validate_expression_postfix', models.TextField(blank=True, null=True)),
                ('identifiers', models.CharField(blank=True, max_length=150, null=True)),
                ('component_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='master.ComponentType')),
                ('query', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reportview.Query')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_params', to='reportview.Report')),
                ('widget_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='master.WidgetType')),
            ],
            options={
                'verbose_name': 'ReportParamField',
                'verbose_name_plural': 'ReportParamFields',
            },
        ),
        migrations.CreateModel(
            name='ReportPDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('iconcls', models.CharField(blank=True, choices=[(b'add', b'Add'), (b'albums', b'Albums'), (b'logo-android', b'Android'), (b'logo-angular', b'Angular'), (b'aperture', b'Aperture'), (b'logo-apple', b'Apple'), (b'apps', b'Apps'), (b'archive', b'Archive'), (b'barcode', b'Barcode'), (b'basket', b'Basket'), (b'bicycle', b'Bicycle'), (b'logo-bitcoin', b'Bitcoin'), (b'bonfire', b'Bonefire'), (b'book', b'Book'), (b'bookmark', b'Bookmark'), (b'bookmarks', b'Bookmarks'), (b'briefcase', b'Briefcase'), (b'calculator', b'Calculator'), (b'calendar', b'Calendar'), (b'card', b'Card'), (b'cash', b'Cash'), (b'clock', b'Clock'), (b'cloud', b'Cloud'), (b'codepen', b'Codepen'), (b'construct', b'Construct'), (b'contact', b'Contact'), (b'copy', b'Copy'), (b'create', b'Create'), (b'cube', b'Cube'), (b'desktop', b'Desktop'), (b'disc', b'Disc'), (b'document', b'Document'), (b'flame', b'Flame'), (b'flower', b'Flower'), (b'floder', b'Floder'), (b'globe', b'Globe'), (b'grid', b'Grid'), (b'help-buoy', b'Help-Buoy'), (b'home', b'Home'), (b'images', b'Images'), (b'information-circle', b'Information-Circle'), (b'keypad', b'Keypad'), (b'laptop', b'Laptop'), (b'list-box', b'List-Box'), (b'lock', b'Lock')], max_length=100, null=True)),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reportview.Report')),
                ('report_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reportview.ReportAction')),
            ],
            options={
                'verbose_name': 'ReportPDF',
                'verbose_name_plural': 'ReportPDFs',
            },
        ),
        migrations.CreateModel(
            name='ReportPrintFormatAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('expression', models.TextField(blank=True, null=True)),
                ('expression_postfix', models.TextField(blank=True, null=True)),
                ('iconcls', models.CharField(blank=True, choices=[(b'add', b'Add'), (b'albums', b'Albums'), (b'logo-android', b'Android'), (b'logo-angular', b'Angular'), (b'aperture', b'Aperture'), (b'logo-apple', b'Apple'), (b'apps', b'Apps'), (b'archive', b'Archive'), (b'barcode', b'Barcode'), (b'basket', b'Basket'), (b'bicycle', b'Bicycle'), (b'logo-bitcoin', b'Bitcoin'), (b'bonfire', b'Bonefire'), (b'book', b'Book'), (b'bookmark', b'Bookmark'), (b'bookmarks', b'Bookmarks'), (b'briefcase', b'Briefcase'), (b'calculator', b'Calculator'), (b'calendar', b'Calendar'), (b'card', b'Card'), (b'cash', b'Cash'), (b'clock', b'Clock'), (b'cloud', b'Cloud'), (b'codepen', b'Codepen'), (b'construct', b'Construct'), (b'contact', b'Contact'), (b'copy', b'Copy'), (b'create', b'Create'), (b'cube', b'Cube'), (b'desktop', b'Desktop'), (b'disc', b'Disc'), (b'document', b'Document'), (b'flame', b'Flame'), (b'flower', b'Flower'), (b'floder', b'Floder'), (b'globe', b'Globe'), (b'grid', b'Grid'), (b'help-buoy', b'Help-Buoy'), (b'home', b'Home'), (b'images', b'Images'), (b'information-circle', b'Information-Circle'), (b'keypad', b'Keypad'), (b'laptop', b'Laptop'), (b'list-box', b'List-Box'), (b'lock', b'Lock')], max_length=100, null=True)),
                ('report_type', models.CharField(blank=True, choices=[(b'onlinereport', b'OnlineReport'), (b'offlinereport', b'OfflineReport'), (b'displayreport', b'Displayreport')], max_length=20, null=True)),
                ('report_params', models.CharField(blank=True, max_length=1024, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reportview.Report')),
                ('report_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='print_formats', to='reportview.ReportAction')),
            ],
            options={
                'verbose_name': 'PrintFormatAction',
                'verbose_name_plural': 'PrintFormatActions',
            },
        ),
        migrations.CreateModel(
            name='ReportSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('expression', models.TextField(blank=True, null=True)),
                ('iconcls', models.CharField(blank=True, choices=[(b'add', b'Add'), (b'albums', b'Albums'), (b'logo-android', b'Android'), (b'logo-angular', b'Angular'), (b'aperture', b'Aperture'), (b'logo-apple', b'Apple'), (b'apps', b'Apps'), (b'archive', b'Archive'), (b'barcode', b'Barcode'), (b'basket', b'Basket'), (b'bicycle', b'Bicycle'), (b'logo-bitcoin', b'Bitcoin'), (b'bonfire', b'Bonefire'), (b'book', b'Book'), (b'bookmark', b'Bookmark'), (b'bookmarks', b'Bookmarks'), (b'briefcase', b'Briefcase'), (b'calculator', b'Calculator'), (b'calendar', b'Calendar'), (b'card', b'Card'), (b'cash', b'Cash'), (b'clock', b'Clock'), (b'cloud', b'Cloud'), (b'codepen', b'Codepen'), (b'construct', b'Construct'), (b'contact', b'Contact'), (b'copy', b'Copy'), (b'create', b'Create'), (b'cube', b'Cube'), (b'desktop', b'Desktop'), (b'disc', b'Disc'), (b'document', b'Document'), (b'flame', b'Flame'), (b'flower', b'Flower'), (b'floder', b'Floder'), (b'globe', b'Globe'), (b'grid', b'Grid'), (b'help-buoy', b'Help-Buoy'), (b'home', b'Home'), (b'images', b'Images'), (b'information-circle', b'Information-Circle'), (b'keypad', b'Keypad'), (b'laptop', b'Laptop'), (b'list-box', b'List-Box'), (b'lock', b'Lock')], max_length=100, null=True)),
                ('epost_target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_epost', to='transactionview.Transactionview')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rpsubmit', to='reportview.Report')),
                ('report_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reportview.ReportAction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reportepostmap',
            name='reportsubmit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportview.ReportSubmit'),
        ),
        migrations.AddField(
            model_name='reportepostmap',
            name='source_ui_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_epost_source', to='reportview.ReportField'),
        ),
        migrations.AddField(
            model_name='reportepostmap',
            name='target_ui_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_epost_target', to='transactionview.Component'),
        ),
        migrations.AddField(
            model_name='report',
            name='dont_repeat_reference_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reportview.ReportField'),
        ),
        migrations.AddField(
            model_name='report',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportview_projects', to='project.Project'),
        ),
        migrations.AddField(
            model_name='query',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_queries', to='reportview.Report'),
        ),
    ]
