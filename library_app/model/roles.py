from django.db import models


class Roles(models.Model):

    #  Fields
    name = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return str(self.pk)
