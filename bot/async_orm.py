from bot.models import TgUser, Contestant
from asgiref.sync import sync_to_async


TgUser_get = sync_to_async(TgUser.objects.get)
TgUser_create = sync_to_async(TgUser.objects.create)

Contestant_get = sync_to_async(Contestant.objects.get)
Contestant_create = sync_to_async(Contestant.objects.create)
