# Generated by Django 4.2.7 on 2024-01-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0014_results_away_team_win_results_draw_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritescalendar',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]