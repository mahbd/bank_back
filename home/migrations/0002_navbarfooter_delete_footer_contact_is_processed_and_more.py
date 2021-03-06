# Generated by Django 4.0.5 on 2022-06-28 01:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavbarFooter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='navbar_icons')),
                ('extra', models.TextField(blank=True, null=True)),
                ('is_navbar', models.BooleanField(default=False)),
                ('is_footer', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.navbarfooter')),
            ],
        ),
        migrations.DeleteModel(
            name='Footer',
        ),
        migrations.AddField(
            model_name='contact',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='submission_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 6, 28, 1, 50, 2, 658195, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Navbar',
        ),
    ]
