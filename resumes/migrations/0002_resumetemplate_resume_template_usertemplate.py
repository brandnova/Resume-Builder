# Generated by Django 5.1.4 on 2024-12-17 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('preview_image', models.ImageField(upload_to='template_previews/')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('html_content', models.TextField(help_text='Enter the complete HTML template code')),
                ('css_content', models.TextField(blank=True, help_text='Additional CSS styles')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resumes.resumetemplate'),
        ),
        migrations.CreateModel(
            name='UserTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('payment_reference', models.CharField(blank=True, max_length=100)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resumetemplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'template')},
            },
        ),
    ]
