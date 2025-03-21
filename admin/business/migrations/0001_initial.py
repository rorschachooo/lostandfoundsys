# Generated by Django 2.2.25 on 2025-03-15 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(help_text='Slideshow number', primary_key=True, serialize=False, verbose_name='Slideshow number')),
                ('img', models.CharField(blank=True, help_text='picture', max_length=255, null=True, verbose_name='picture ')),
                ('url', models.CharField(blank=True, help_text='Link address', max_length=255, null=True, verbose_name='Link address ')),
                ('index_radio', models.CharField(blank=True, help_text='Is it home page', max_length=255, null=True, verbose_name='Is it home page ')),
            ],
            options={
                'verbose_name': 'Slideshow',
                'verbose_name_plural': 'Slideshow',
                'db_table': 'banner',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(help_text='Claim Number', primary_key=True, serialize=False, verbose_name='Claim Number')),
                ('user_id', models.IntegerField(blank=True, help_text='Claim User', null=True, verbose_name='Claim User')),
                ('name', models.CharField(blank=True, help_text='Claiming items', max_length=255, null=True, verbose_name='Claiming items ')),
                ('img', models.CharField(blank=True, help_text='Item Image', max_length=255, null=True, verbose_name='Item Image ')),
                ('biz_user_id', models.IntegerField(blank=True, help_text='Pickup Person', null=True, verbose_name='Pickup Person')),
                ('goodid', models.IntegerField(blank=True, help_text='Item Number', null=True, verbose_name='Item Number')),
            ],
            options={
                'verbose_name': 'Information to be claimed',
                'verbose_name_plural': 'Information to be claimed',
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(help_text='number', primary_key=True, serialize=False, verbose_name='number')),
                ('name', models.CharField(blank=True, help_text='Category Name', max_length=255, null=True, verbose_name='Category Name ')),
            ],
            options={
                'verbose_name': 'Item Type',
                'verbose_name_plural': 'Item Type',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Lost',
            fields=[
                ('id', models.AutoField(help_text='number', primary_key=True, serialize=False, verbose_name='number')),
                ('category_id', models.IntegerField(blank=True, help_text='Item Classification', null=True, verbose_name='Item Classification')),
                ('name', models.CharField(blank=True, help_text='Item Name', max_length=255, null=True, verbose_name='Item Name ')),
                ('img', models.CharField(blank=True, help_text='Item Image', max_length=255, null=True, verbose_name='Item Image ')),
                ('content', models.TextField(blank=True, help_text='Item Description', null=True, verbose_name='Item Description ')),
                ('address', models.CharField(blank=True, help_text='Lost location', max_length=255, null=True, verbose_name='Lost location ')),
                ('time', models.CharField(blank=True, help_text='Lost time', max_length=255, null=True, verbose_name='Lost time ')),
                ('phone', models.CharField(blank=True, help_text='Contact Details', max_length=255, null=True, verbose_name='Contact Details ')),
                ('user_id', models.IntegerField(blank=True, help_text='Publisher', null=True, verbose_name='Publisher')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='Release time', null=True, verbose_name='Release time')),
            ],
            options={
                'verbose_name': 'Report lost items',
                'verbose_name_plural': 'Report lost items',
                'db_table': 'lost',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(help_text='number', primary_key=True, serialize=False, verbose_name='number')),
                ('username', models.CharField(blank=True, help_text='Log in to your account', max_length=255, null=True, verbose_name='Log in to your account ')),
                ('name', models.CharField(blank=True, help_text='Name', max_length=255, null=True, verbose_name='Name ')),
                ('user_id', models.IntegerField(blank=True, help_text='User', null=True, verbose_name='User ')),
                ('phone', models.CharField(blank=True, help_text='phone number', max_length=255, null=True, verbose_name='phone number ')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'user',
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(help_text='Claim Number', primary_key=True, serialize=False, verbose_name='Claim Number')),
                ('name', models.CharField(blank=True, help_text='Claim Number', max_length=255, null=True, verbose_name='Claim Number ')),
                ('content', models.TextField(blank=True, help_text='Claim details', null=True, verbose_name='Claim details ')),
                ('state_radio', models.CharField(blank=True, help_text='Order status, claiming|confirmed as lost|returned|cancelled', max_length=255, null=True, verbose_name='Order status, claiming|confirmed as lost|returned|cancelled ')),
                ('user_id', models.IntegerField(blank=True, help_text='Claim User', null=True, verbose_name='Claim User')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='Application period', null=True, verbose_name='Application period')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Update time')),
                ('biz_user_id', models.IntegerField(blank=True, help_text='Lost and found person', null=True, verbose_name='Lost and found person')),
                ('goodids', models.CharField(blank=True, help_text='Item Number', max_length=255, null=True, verbose_name='Item Number ')),
            ],
            options={
                'verbose_name': 'Lost and found records',
                'verbose_name_plural': 'Lost and found records',
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(help_text='number', primary_key=True, serialize=False, verbose_name='number')),
                ('category_id', models.IntegerField(blank=True, help_text='Item Classification', null=True, verbose_name='Item Classification ')),
                ('name', models.CharField(blank=True, help_text='Item Name', max_length=255, null=True, verbose_name='Item Name ')),
                ('img', models.CharField(blank=True, help_text='Item Image', max_length=255, null=True, verbose_name='Item Image ')),
                ('content', models.TextField(blank=True, help_text='Item Description', null=True, verbose_name='Item Description ')),
                ('address', models.CharField(blank=True, help_text='Pickup Location', max_length=255, null=True, verbose_name='Pickup Location ')),
                ('time', models.CharField(blank=True, help_text='Pickup time', max_length=255, null=True, verbose_name='Pickup time ')),
                ('user_id', models.IntegerField(blank=True, help_text='Publisher', null=True, verbose_name='Publisher ')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='Release time ', null=True, verbose_name='Release time')),
            ],
            options={
                'verbose_name': 'Lost and Found',
                'verbose_name_plural': 'Lost and Found',
                'db_table': 'recruit',
            },
        ),
    ]
