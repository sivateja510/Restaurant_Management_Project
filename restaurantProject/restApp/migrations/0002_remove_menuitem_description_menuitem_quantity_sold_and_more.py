# Generated by Django 5.0.7 on 2024-07-16 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='description',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='quantity_sold',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
