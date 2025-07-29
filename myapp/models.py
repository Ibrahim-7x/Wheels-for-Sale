from django.db import models

class Bulk(models.Model):
    start_time = models.CharField(max_length=50)
    hangUp_time = models.CharField(max_length=50)
    cli = models.CharField(max_length=100)
    call_status = models.CharField(max_length=100)
    talk_time = models.CharField(max_length=100)
    login_id = models.CharField(max_length=100)
    citrix_id = models.CharField(max_length=100)
    call_picked = models.BooleanField(default=False)

class Test_Bulk(models.Model):
    start_time = models.CharField(max_length=50)
    hangUp_time = models.CharField(max_length=50)
    cli = models.CharField(max_length=100)
    call_status = models.CharField(max_length=100)
    talk_time = models.CharField(max_length=100)
    login_id = models.CharField(max_length=100)
    citrix_id = models.CharField(max_length=100)
    call_picked = models.BooleanField(default=False)


class CallPool(models.Model):
    bulk_table = models.ForeignKey('Bulk', on_delete=models.CASCADE)
    citrix_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        unique_together = ('bulk_table',)

class Test_CallPool(models.Model):
    bulk_table = models.ForeignKey('Test_Bulk', on_delete=models.CASCADE)
    citrix_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        unique_together = ('bulk_table',)

class DailyCallLog(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('citrix_id', 'date')

class Test_DailyCallLog(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('citrix_id', 'date')



class DailyCallLogHistory(models.Model):
    citrix_id = models.CharField(max_length=100)
    date = models.DateField()
    call_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('citrix_id','date')

class Test_DailyCallLogHistory(models.Model):
    citrix_id = models.CharField(max_length=100)
    date = models.DateField()
    call_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('citrix_id','date')




class WeeklyCallLog(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    week_start = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('citrix_id', 'week_start')


class Test_WeeklyCallLog(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    week_start = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('citrix_id', 'week_start')
    

class WeeklyCallLogHistory(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('citrix_id', 'week_start')


class Test_WeeklyCallLogHistory(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('citrix_id', 'week_start')


class MonthlyCallLog(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    month_start = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('citrix_id','month_start')


class Test_MonthlyCallLog(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    month_start = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('citrix_id','month_start')

class MonthlyCallLogHistory(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    month_start = models.DateField()
    month_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('citrix_id', 'month_start')


class Test_MonthlyCallLogHistory(models.Model):
    citrix_id = models.CharField(max_length=100)
    call_count = models.IntegerField()
    month_start = models.DateField()
    month_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('citrix_id', 'month_start')



