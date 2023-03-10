# Generated by Django 3.2 on 2022-12-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('mobile_number', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Mobile Number')),
                ('is_active', models.BooleanField(default=True)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_supervisor', models.BooleanField(default=False)),
                ('address', models.TextField(blank=True, default='')),
                ('tax_number', models.CharField(db_index=True, default='097947', max_length=7)),
                ('account_number', models.CharField(db_index=True, default='141800430', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
