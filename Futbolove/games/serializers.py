""" Serializery są wykorzystywane do mapowania modeli na dane, które mogą być następnie używane do generowania odpowiedzi
    API. Mogą być łatwo przesyłane w formie JSON wszystkie pola zdefiniowane w modelu
    zostaną uwzględnione w danych wyjściowych serializatora."""
from rest_framework import serializers
from .models import League, Team, Match, Comment, Results, Favorite, FavoritesCalendar, Bet


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['reason', 'result', 'match']


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = '__all__'
        read_only_fields = ['results', 'home_team_win', 'draw', 'away_team_win']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['league']


class FavoritesCalendarSerializer(serializers.ModelSerializer):
    upcoming_matches = serializers.SerializerMethodField()

    class Meta:
        model = FavoritesCalendar
        fields = ['id', 'user', 'team', 'upcoming_matches']
        read_only_fields = ['id', 'user', 'team', 'upcoming_matches']

    def get_upcoming_matches(self, obj):
        return MatchSerializer(obj.get_upcoming_matches(), many=True).data
