"""Models of the Items and Images for storing in the database."""
from __future__ import unicode_literals

from django.db import models


class Item(models.Model):
    """Table for an item."""

    name = models.CharField(max_length=250, )
    description = models.TextField()
    link = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    contact = models.TextField()

    def __str__(self):
        """Return value for the obj."""
        return self.name


class ItemImage(models.Model):
    """An item's image."""

    item = models.ForeignKey(Item,)
    image = models.FileField("ItemImages", upload_to="items/%Y/%m/%d")

    def __str__(self):
        """Return value for the obj."""
        return self.item
