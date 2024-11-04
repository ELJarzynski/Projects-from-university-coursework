from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeagueViewSet, TeamViewSet, MatchViewSet, CommentViewSet, ResultsViewSet, FavoriteViewSet, \
    FavoritesCalendarViewSet, BetViewSet

router = DefaultRouter()
router.register(r'bets', BetViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'results', ResultsViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'favorites_schedule', FavoritesCalendarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
