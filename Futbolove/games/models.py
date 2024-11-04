from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
Comment_STATUS = (
    ('pending', 'Waiting for review'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)


class League(models.Model):
    class Meta:
        verbose_name_plural = "League"

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    class Meta:
        verbose_name_plural = "Teams"

    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Team)
def team_country(sender, instance, **kwargs):
    if not instance.country:
        instance.country = instance.league.country


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"

    league = models.ForeignKey(League, on_delete=models.CASCADE, default=1)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"


class Results(models.Model):
    class Meta:
        verbose_name_plural = "Results"
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='result_home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='result_away_matches', on_delete=models.CASCADE)
    date = models.DateTimeField()
    result = models.CharField(max_length=10, blank=True, null=True)

    # Stats
    possession_home_team = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    possession_away_team = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    shots_on_goal_home_team = models.IntegerField(blank=True, null=True)
    shots_on_goal_away_team = models.IntegerField(blank=True, null=True)
    fouls_home_team = models.IntegerField(blank=True, null=True)
    fouls_away_team = models.IntegerField(blank=True, null=True)

    # Bets
    home_team_win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    away_team_win = models.IntegerField(default=0)

    def possession(self, *args, **kwargs):
        if self.possession_home_team is not None:
            self.possession_away_team = 100 - self.possession_home_team

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"


class Bet(models.Model):
    MATCH_CHOICES = [
        ('1', 'Home Team Wins'),
        ('X', 'Draw'),
        ('2', 'Away Team Wins'),
    ]

    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=True, blank=True)
    results = models.ForeignKey('Results', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    result = models.CharField(max_length=1, choices=MATCH_CHOICES, null=True, blank=True)
    home_team_win = models.IntegerField(default=0, blank=True, null=True)
    draw = models.IntegerField(default=0, blank=True, null=True)
    away_team_win = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        user_str = self.user.username if self.user else "Unknown User"
        match_str = str(self.match) if self.match else "Unknown Match"
        result_str = self.result if self.result else "No Result"
        return f"{user_str} - {match_str} - {result_str}"

    def save(self, *args, **kwargs):
        if not self.pk:
            existing_bets = Bet.objects.filter(match=self.match)

            # Zaktualizuj wartości na podstawie istniejących zakładów
            self.home_team_win = sum(1 for bet in existing_bets if bet.result == '1')
            self.draw = sum(1 for bet in existing_bets if bet.result == 'X')
            self.away_team_win = sum(1 for bet in existing_bets if bet.result == '2')

        if self.result:
            if self.result == '1':
                self.home_team_win += 1
            elif self.result == 'X':
                self.draw += 1
            elif self.result == '2':
                self.away_team_win += 1

        super().save(*args, **kwargs)


class Comment(models.Model):
    class Meta:
        verbose_name_plural = "Comment Panel"

    result = models.ForeignKey('Results', on_delete=models.CASCADE, null=True, blank=True)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(choices=Comment_STATUS, max_length=30, default='pending')

    def __str__(self):
        return f'Comment ID: {self.id}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', related_name='favorites', on_delete=models.CASCADE)
    league = models.ForeignKey('League', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.team)

    def save(self, *args, **kwargs):
        if self.team and not self.league:
            self.league = self.team.league
        super().save(*args, **kwargs)


class FavoritesCalendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', related_name='calendar_teams', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def get_upcoming_matches(self):
        now = timezone.now()

        home_matches = Match.objects.filter(
            date__gte=now,
            home_team=self.team
        ).exclude(
            date__lt=now
        ).order_by('date')[:3]

        away_matches = Match.objects.filter(
            date__gte=now,
            away_team=self.team
        ).exclude(
            date__lt=now
        ).order_by('date')[:3]

        upcoming_matches = list(home_matches) + list(away_matches)
        upcoming_matches.sort(key=lambda x: x.date)

        return upcoming_matches[:3]

    def __str__(self):
        return f"{self.user.username}'s Favorites Calendar for {self.team.name}"


@receiver(post_save, sender=Favorite)
def add_favorite_to_calendar(sender, instance, created, **kwargs):
    if created:
        FavoritesCalendar.objects.create(user=instance.user, team=instance.team)


@receiver(post_delete, sender=Favorite)
def remove_favorite_from_calendar(sender, instance, **kwargs):
    try:
        calendar_entry = FavoritesCalendar.objects.get(user=instance.user, team=instance.team)
        calendar_entry.delete()
    except FavoritesCalendar.DoesNotExist:
        pass

