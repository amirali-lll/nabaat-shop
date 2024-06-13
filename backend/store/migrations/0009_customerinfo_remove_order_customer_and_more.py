# Generated by Django 5.0.2 on 2024-06-13 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_customer_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='address',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='order',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='store.order'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
