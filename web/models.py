from django.db import models

class Footprint(models.Model):
    footprint_id = models.AutoField(primary_key=True, blank=True, null=False)
    latitude = models.TextField()  # This field type is a guess.
    longitude = models.TextField()  # This field type is a guess.
    trip = models.ForeignKey('Trip', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Footprint'


class Map(models.Model):
    map_id = models.AutoField(primary_key=True, blank=True, null=False)
    map_name = models.TextField(blank=True, null=True)
    map_nw_latitude = models.FloatField()
    map_nw_longitude = models.FloatField()
    map_se_latitude = models.FloatField()
    map_se_longitude = models.FloatField()

    class Meta:
        db_table = 'Map'


class SheepEntry(models.Model):
    sheep_entry_id = models.AutoField(primary_key=True, blank=True, null=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    total_calculated = models.IntegerField(blank=True, null=True)
    total_spotted = models.IntegerField(blank=True, null=True)
    blacks = models.IntegerField(blank=True, null=True)
    whites = models.IntegerField(blank=True, null=True)
    red_ties = models.IntegerField(blank=True, null=True)
    yellow_ties = models.IntegerField(blank=True, null=True)
    green_ties = models.IntegerField(blank=True, null=True)
    blue_ties = models.IntegerField(blank=True, null=True)
    red_ear = models.IntegerField(blank=True, null=True)
    yellow_ear = models.IntegerField(blank=True, null=True)
    green_ear = models.IntegerField(blank=True, null=True)
    trip = models.ForeignKey('Trip', models.DO_NOTHING)

    class Meta:
        db_table = 'Sheep_entry'


class SheepSpottedFrom(models.Model):
    location_id = models.AutoField(primary_key=True, blank=True, null=False)
    sheep_entry = models.ForeignKey(SheepEntry, models.DO_NOTHING)
    spotted_from_latitude = models.FloatField()
    spotted_from_longitude = models.FloatField()

    class Meta:
        db_table = 'Sheep_spotted_from'


class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True, blank=True, null=False)
    map = models.ForeignKey(Map, models.DO_NOTHING)
    trip_date_time = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Trip'


class PredatorLocation(models.Model):
    predator_id = models.AutoField(primary_key=True, blank=True, null=False)
    type = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    spottedfrom_latitude = models.FloatField()
    spottedfrom_longitude = models.FloatField()
    trip = models.ForeignKey('Trip', models.DO_NOTHING)

    class Meta:
        db_table = 'Predator_location'


class Drive(models.Model):
    drive_id = models.TextField(primary_key=True, blank=True, null=False)
    
    class Meta:
        db_table = 'Drive'

class DeadSheep(models.Model):
    dead_sheep_id = models.AutoField(primary_key=True, blank=True, null=False)
    dead_sheep_latitude = models.FloatField()
    dead_sheep_longitude = models.FloatField()
    dead_sheep_spottedfrom_latitude = models.FloatField()
    dead_sheep_spottedfrom_longitude = models.FloatField()
    trip = models.ForeignKey('Trip', models.DO_NOTHING)

    class Meta:
        db_table = 'Dead_sheep'

class AndroidMetadata(models.Model):
    locale = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'android_metadata'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
