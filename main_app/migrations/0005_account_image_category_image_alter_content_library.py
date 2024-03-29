# Generated by Django 4.1 on 2022-08-16 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_account_user_alter_file_modification_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.ImageField(null=True, upload_to='user_images/'),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='category_images/'),
        ),
        migrations.AlterField(
            model_name='content',
            name='library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contents', to='main_app.library'),
        ),
    ]
