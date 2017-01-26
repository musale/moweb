"""Super admin site config."""
from django.contrib import admin

from core.models import Item, ItemImage

admin.site.register(ItemImage)
admin.site.register(Item)
