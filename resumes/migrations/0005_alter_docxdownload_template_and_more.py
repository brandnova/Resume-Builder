# Generated by Django 5.1.4 on 2024-12-18 20:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0004_docxdownload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docxdownload',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resumes.resumetemplate'),
        ),
        migrations.AlterField(
            model_name='pdfdownload',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resumes.resumetemplate'),
        ),
    ]
