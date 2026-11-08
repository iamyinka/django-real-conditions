from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="items/", blank=True)


class Booking(models.Model):
    """Postgres exclusion constraint: one technician can't have overlapping slots."""

    technician = models.IntegerField()
    slot = DateTimeRangeField()

    class Meta:
        constraints = [
            ExclusionConstraint(
                name="no_overlapping_slots",
                expressions=[
                    ("technician", RangeOperators.EQUAL),
                    ("slot", RangeOperators.OVERLAPS),
                ],
            )
        ]
