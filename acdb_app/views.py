from django.shortcuts import render
from acdb_app.models import Player, Event, Position, Game, Move

def landing_page(request):
    total_players = Player.objects.count()
    total_events = Event.objects.count()
    total_positions = Position.objects.count()
    total_games = Game.objects.count()
    total_moves = Move.objects.count()
    context = {
        'total_players': total_players,
        'total_events': total_events,
        'total_positions': total_positions,
        'total_games': total_games,
        'total_moves': total_moves
        }
    return render(request, 'landing.html', context)