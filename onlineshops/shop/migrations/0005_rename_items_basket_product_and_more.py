# Generated by Django 4.2.4 on 2023-10-16 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_basket_iteminorder_review_order_iteminorder_order_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='items',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='iteminbasket',
            old_name='item',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='iteminorder',
            old_name='item',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='item',
            new_name='product',
        ),
    ]
