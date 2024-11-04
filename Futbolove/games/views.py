from rest_framework import viewsets
from .models import League, Team, Match, Comment, Results, Favorite, FavoritesCalendar, Bet
from .serializers import LeagueSerializer, TeamSerializer, MatchSerializer, CommentSerializer, ResultsSerializer, \
    FavoriteSerializer, FavoritesCalendarSerializer, BetSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoritesCalendarViewSet(viewsets.ModelViewSet):
    queryset = FavoritesCalendar.objects.all()
    serializer_class = FavoritesCalendarSerializer
