# Generated by Django 5.0.3 on 2024-04-20 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_review_review'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]