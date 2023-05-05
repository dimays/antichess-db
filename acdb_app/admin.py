from django.contrib import admin

# Register your models here.
from .models import Annotation, Player, Event, Position, Game, Move

admin.site.register(Annotation)
admin.site.register(Player)
admin.site.register(Event)
admin.site.register(Position)
admin.site.register(Game)
admin.site.register(Move)