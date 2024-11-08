# Generated by Django 5.1.2 on 2024-10-29 18:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_order_address_order_branch_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='branch_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
