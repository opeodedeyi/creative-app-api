# Generated by Django 2.2.5 on 2019-12-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20191230_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followlog',
            name='status',
            field=models.CharField(choices=[('following', 'following'), ('unfollowed', 'unfollowed'), ('blocked', 'blocked')], default='following', max_length=30),
        ),
    ]
