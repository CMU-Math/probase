# Generated by Django 3.0.5 on 2020-05-14 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.IntegerField()),
                ('quality', models.IntegerField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='database.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='qualityrating',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='qualityrating',
            name='user',
        ),
        migrations.DeleteModel(
            name='DifficultyRating',
        ),
        migrations.DeleteModel(
            name='QualityRating',
        ),
    ]