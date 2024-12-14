from django.db import models
from ..model.base import Base

class Books(Base):
    title = models.CharField(max_length=155, unique=False, null=True, blank=True)
    author = models.CharField(max_length=155, unique=False, null=True, blank=True)
    isbn = models.CharField(max_length=155, unique=True, null=True, blank=True)
    copies_available = models.IntegerField(unique=False, null=True, blank=True, default=0)

    class Meta:
        db_table = "books"

    def __str__(self):
        return str(self.pk)


