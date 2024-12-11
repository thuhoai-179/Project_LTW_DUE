# Generated by Django 4.2.8 on 2024-12-03 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_category_post_notification_comment_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiated_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]