# Generated by Django 5.1.3 on 2025-03-12 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_alter_content_cast_alter_content_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(choices=[('short_film', 'Short Film'), ('podcast', 'Podcast'), ('documentary', 'Documentary'), ('entertainment', 'Entertainment Project'), ('music', 'Music'), ('education', 'Education'), ('interviews', 'Interviews'), ('animation', 'Animation')], max_length=50),
        ),
    ]
