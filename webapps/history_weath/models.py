from django.db import models

class Lishitianqi(models.Model):
    city = models.CharField(max_length=16)
    date = models.DateField()
    maxt = models.IntegerField()
    mint = models.IntegerField()
    weath = models.CharField(max_length=20)
    windd = models.CharField(max_length=20)
    windp = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lishitianqi'
        unique_together = (('city', 'date'),)


class Citys(models.Model):
    city = models.CharField(primary_key=True, max_length=16)
    hot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'citys'