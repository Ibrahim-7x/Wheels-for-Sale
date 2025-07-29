from django.core.management.base import BaseCommand
from django.db.models import Count
from datetime import date, timedelta

from randomizar.models import (
    Test_CallPool,
    Test_DailyCallLog,
    Test_DailyCallLogHistory,
    Test_WeeklyCallLog,
    Test_WeeklyCallLogHistory,
    Test_MonthlyCallLog,
    Test_MonthlyCallLogHistory,
)


def get_week_start(d):
    return d - timedelta(days=d.weekday())

def get_week_end(d):
    return get_week_start(d) + timedelta(days=6)

def get_month_start(d):
    return d.replace(day=1)

def get_month_end(d):
    next_month = d.replace(day=28) + timedelta(days=4)
    return next_month.replace(day=1) - timedelta(days=1)


class Command(BaseCommand):
    help = "Uploads today's call logs and archives daily, weekly, and monthly logs into history."

    def handle(self, *args, **kwargs):
        today = date.today()
        yesterday = today - timedelta(days=1)

        week_start = get_week_start(today)
        last_week_start = get_week_start(today - timedelta(days=7))
        last_week_end = last_week_start + timedelta(days=6)

        month_start = get_month_start(today)
        last_month_end = get_month_start(today) - timedelta(days=1)
        last_month_start = get_month_start(last_month_end)

        # --- DAILY LOGS ---
        self.stdout.write(self.style.NOTICE("\n📦 Archiving DAILY logs..."))
        for record in Test_DailyCallLog.objects.all():
            Test_DailyCallLogHistory.objects.update_or_create(
                citrix_id=record.citrix_id,
                date=record.date,
                defaults={'call_count': record.call_count}
            )
        Test_DailyCallLog.objects.all().delete()

        today_calls = Test_CallPool.objects.filter(timestamp__date=today)
        daily_data = today_calls.values('citrix_id').annotate(call_count=Count('id'))
        for entry in daily_data:
            Test_DailyCallLog.objects.create(
                citrix_id=entry['citrix_id'],
                call_count=entry['call_count'],
                date=today  # ✅ Save correct log date
            )
        self.stdout.write(self.style.SUCCESS("✅ Daily logs updated."))

        # --- WEEKLY LOGS ---
        self.stdout.write(self.style.NOTICE("\n📦 Archiving WEEKLY logs..."))
        for record in Test_WeeklyCallLog.objects.filter(week_start__lt=week_start):
            Test_WeeklyCallLogHistory.objects.update_or_create(
                citrix_id=record.citrix_id,
                week_start=record.week_start,
                week_end=record.week_start + timedelta(days=6),
                defaults={'call_count': record.call_count}
            )
        Test_WeeklyCallLog.objects.all().delete()

        weekly_data = Test_CallPool.objects.filter(timestamp__date__gte=week_start, timestamp__date__lte=today)
        weekly_grouped = weekly_data.values('citrix_id').annotate(call_count=Count('id'))
        for entry in weekly_grouped:
            Test_WeeklyCallLog.objects.create(
                citrix_id=entry['citrix_id'],
                week_start=week_start,
                call_count=entry['call_count']
            )
        self.stdout.write(self.style.SUCCESS("✅ Weekly logs updated."))

        # --- MONTHLY LOGS ---
        self.stdout.write(self.style.NOTICE("\n📦 Archiving MONTHLY logs..."))
        for record in Test_MonthlyCallLog.objects.filter(month_start__lt=month_start):
            Test_MonthlyCallLogHistory.objects.update_or_create(
                citrix_id=record.citrix_id,
                month_start=record.month_start,
                month_end=get_month_end(record.month_start),
                defaults={'call_count': record.call_count}
            )
        Test_MonthlyCallLog.objects.all().delete()

        monthly_data = Test_CallPool.objects.filter(timestamp__date__gte=month_start, timestamp__date__lte=today)
        monthly_grouped = monthly_data.values('citrix_id').annotate(call_count=Count('id'))
        for entry in monthly_grouped:
            Test_MonthlyCallLog.objects.create(
                citrix_id=entry['citrix_id'],
                month_start=month_start,
                call_count=entry['call_count']
            )
        self.stdout.write(self.style.SUCCESS("✅ Monthly logs updated."))
