# Generated by Django 5.1.2 on 2024-10-31 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('оплачен', 'Оплачен'), ('доставляется', 'Доставляется'), ('доставлен', 'Доставлен')], default='Оплачен', max_length=20),
        ),
    ]