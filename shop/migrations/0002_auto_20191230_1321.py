--4# Generated by Django 2.2.4 on 2019-12-30 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='catogary',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='subcatogary',
            field=models.CharField(default='', max_length=50),
        ),
    ]
