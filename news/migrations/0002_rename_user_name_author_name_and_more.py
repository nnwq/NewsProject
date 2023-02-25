# Generated by Django 4.1.7 on 2023-02-22 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='user_rating',
            new_name='rating',
        ),
        migrations.AlterField(
            model_name='post',
            name='type_choice',
            field=models.CharField(choices=[('AR', 'Article'), ('NW', 'News')], default='News', max_length=10),
        ),
    ]