from django.db import models
from django.contrib.auth.models import User


class Court(models.Model):
    name = models.CharField(max_length=100, verbose_name='场地名称')
    description = models.TextField(blank=True, verbose_name='场地描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '场地'
        verbose_name_plural = '场地'
        ordering = ['id']

    def __str__(self):
        return self.name


class CourtAvailability(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='availabilities', verbose_name='场地')
    date = models.DateField(verbose_name='日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '场地可用时间段'
        verbose_name_plural = '场地可用时间段'
        unique_together = ['court', 'date']
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.court.name} - {self.date} {self.start_time}-{self.end_time}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', '有效'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='用户')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='bookings', verbose_name='场地')
    date = models.DateField(verbose_name='预约日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '预约'
        verbose_name_plural = '预约'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.user.username} - {self.court.name} - {self.date} {self.start_time}-{self.end_time}'
