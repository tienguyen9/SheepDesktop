from django.db import models

# Create your models here.

class PredatorArea(models.Model):
    predator_id = models.AutoField(primary_key=True, blank=True, null=False)
    predator_json_string = models.TextField()

    class Meta:
        app_label='desktop'
        db_table = 'Predator_area'
        managed = True

class ReportEntry(models.Model):
    report_id = models.AutoField(primary_key=True, blank=True, null=False)
    description = models.TextField()
    trip = models.ForeignKey('web.Trip', models.DO_NOTHING)
    class Meta:
        app_label='desktop'
        db_table = 'Report_entry'
        managed = True