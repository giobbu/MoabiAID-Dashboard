from django.contrib.gis.db import models
from django.contrib.gis import geos
from polymorphic.models import PolymorphicModel

import django.contrib.postgres.indexes as psql_indexes


# Create your models here.

class Truck(models.Model):
    """
    A truck
    
    :param models: [description]
    :type models: [type]
    """

    # Truck identifiers
    obu_id = models.BigIntegerField()
    measurement_date = models.DateField()

    # Truck attributes
    weight_category = models.PositiveSmallIntegerField(null=True) #TODO: verify this
    average_velocity = models.FloatField(null=True)
    country_code = models.CharField(max_length=3, null=True) #TODO: update according to maximal length of a country code
    euro_value = models.PositiveSmallIntegerField(null=True) # TODO: check if we need to handle possible 6d and RDE values

    # Geographic information
    last_position = models.PointField()
    route = models.LineStringField() #TODO: how to handle position, direction and timestamp associations
    directions = None # How to store?

    class Meta:
        unique_together = ['obu_id', 'measurement_date']
        required_db_features = ['gis_enabled']
        required_db_vendor = 'postgresql'
        indexes = [
            psql_indexes.BrinIndex(fields=['measurement_date'], name='daily_summary_idx')
        ]


class Commune(models.Model):

    # Administrative data
    name = models.TextField()
    population = models.PositiveIntegerField()
    postal_code = models.PositiveSmallIntegerField()
    area = models.PositiveSmallIntegerField()

    # Geographical features

    center = models.PointField()
    boundaries = models.MultiPolygonField()

    #etc.

    def get_boundaries(self):
        """
        Retrieves the commune boundaries and name
        """
        return {'name': self.name, 'borders': self.boundaries}

    def save(self, *args, **kwargs):
        # if boundaries ends up as a Polgon, make it into a MultiPolygon
        if self.boundaries and isinstance(self.boundaries, geos.Polygon):
            self.boundaries = geos.MultiPolygon(self.boundaries)

        super(Commune).save(*args, **kwargs)

    class Meta:
        required_db_features = ['gis_enabled']
        required_db_vendor = 'postgresql'

class Street(models.Model):

    name = models.TextField()
    speed_limit = models.PositiveSmallIntegerField()

    commune = models.ForeignKey("dashboard.Commune", on_delete=models.CASCADE, related_name='streets') # Every street belongs to a commune

    path = models.MultiLineStringField() # Contains LineStrings in segments; TODO: determine wether we store this implicitly or construct from segment linestrings

    def add_segment(self, segment):
        pass # TODO: this method should validate wether the segment can be added and update the MultiLineString field

    class Meta:
        required_db_features = ['gis_enabled']
        required_db_vendor = 'postgresql'

class StreetSegment(models.Model):

    # TODO: enforce that a segment should either belong to a street or another segment, but not both
    street = models.ForeignKey('dashboard.Street', on_delete=models.CASCADE, related_name='segments', null=True) # A street consists of several segments
    parent_segment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_segments', null=True)

    ROAD_TYPES = [('DI', 'Dirt'), ('ASP', 'Asphalt'), ('CON', 'Concrete')]
    road_type = models.CharField(max_length=3, choices=ROAD_TYPES)

    segment_path = models.LineStringField() #TODO: find a way to enforce that the path of a segment should be a subset 

    class Meta:
        required_db_features = ['gis_enabled']
        required_db_vendor = 'postgresql'


class TrafficEvent(PolymorphicModel):

    resolved = models.BooleanField(default=False)

    report_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    position = models.PointField()

    class Meta:
        required_db_features = ['gis_enabled']
        required_db_vendor = 'postgresql'

class RoadWorks(TrafficEvent): # This is an example, maybe this should better be a super class for all events concerning a full road segment

    description = models.TextField(default='N.A.')
    start_date = models.DateField()
    end_date = models.DateField()

    street_segments = models.ManyToManyField(StreetSegment)

    class Meta:
        required_db_features = ['gis_enabled']
        required_db_vendor = 'postgresql'