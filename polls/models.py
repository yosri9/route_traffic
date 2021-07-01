from django.db import models


class Data(models.Model):
    cin = models.IntegerField(  )
    altitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    speed = models.CharField(max_length=100, null=True)
    ENGINE_RPM = models.CharField(max_length=100, null=True)
    ENGINE_LOAD = models.CharField(max_length=100, null=True)
    AmbientAirTemp = models.CharField(max_length=100, null=True)
    ThrottlePos = models.CharField(max_length=100, null=True)
    insFuel = models.CharField(max_length=100, null=True)
    valX = models.FloatField(null=True)
    valY = models.FloatField(null=True)
    valZ = models.FloatField(null=True)
    zone = models.CharField(max_length=100, null=True)
    time = models.DateTimeField( )

    class Meta:
        unique_together = (("cin", "time"),)
class AverageData(models.Model):
    first_node_altitude = models.FloatField(null=True)
    first_node_longitude = models.FloatField(null=True)
    end_node_altitude = models.FloatField(null=True)
    end_node_longitude = models.FloatField(null=True)
    distance_between_end_node_and_point = models.FloatField(null=True)
    road_length = models.FloatField(null=True)

    averageSpeed = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (("id"),)

class AverageDataPerSegment(models.Model):
    first_node_altitude = models.FloatField(null=True)
    first_node_longitude = models.FloatField(null=True)
    end_node_altitude = models.FloatField(null=True)
    end_node_longitude = models.FloatField(null=True)
    counted_value = models.FloatField(null=True)

    averageSpeed = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (("id"),)



