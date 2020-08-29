# Generated by Django 2.2.4 on 2020-08-21 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wish_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Granted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('granted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='granted_items_by_user', to='wish_app.User')),
                ('granted_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='granted_items', to='wish_app.Wish')),
            ],
        ),
    ]
