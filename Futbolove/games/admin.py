from django.contrib import admin
from .models import Team, Match, League, Comment, Results, Favorite, FavoritesCalendar, Bet


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'result', 'match', 'reason', 'status')
    list_filter = ('status', 'result__league', 'match__league')


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'user', 'result', 'home_team_win', 'draw', 'away_team_win', 'results')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'country')
    list_filter = ('league', 'country')
    ordering = ['league__name', 'name']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('league', 'home_team', 'away_team', 'date')
    actions = ['move_to_results']
    ordering = ['-date']
    inlines = [CommentInline]

    @admin.action(description='Move selected matches to Results')
    def move_to_results(self, request, queryset):
        for match in queryset:
            results = Results(
                home_team=match.home_team,
                away_team=match.away_team,
                date=match.date,
                league=match.league,
            )
            results.save()

            bets = Bet.objects.filter(match=match)
            for bet in bets:
                if bet.result == '1':
                    results.home_team_win += 1
                elif bet.result == 'X':
                    results.draw += 1
                elif bet.result == '2':
                    results.away_team_win += 1

            for bet in bets:
                user = bet.user
                result_bet = Bet(
                    match=None,
                    results=results,
                    user=user,
                    result=bet.result,
                )
                result_bet.save()

            results.save()

            comments = Comment.objects.filter(match=match)
            for comment in comments:
                result_comment = Comment(
                    result=results,
                    match=None,
                    reason=comment.reason,
                    status=comment.status,
                )
                result_comment.save()
            match.delete()


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('league', 'home_team', 'away_team', 'date', 'result')
    list_filter = ('league', 'date')
    ordering = ['-date']
    inlines = [CommentInline]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'league')


@admin.register(FavoritesCalendar)
class FavoritesCalendarAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'display_upcoming_matches')
    list_filter = ('user', 'team')

    def display_upcoming_matches(self, obj):
        upcoming_matches = obj.get_upcoming_matches()
        return '\n'.join([str(match) for match in upcoming_matches])

    display_upcoming_matches.short_description = 'Upcoming Matches'


