import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Exhibit(models.Model):
    short_name = models.CharField(max_length=40)
    long_name = models.CharField(max_length=100)

    def __str__(self):
        return self.long_name


# class Day(models.Model):
#     order = models.IntegerField()
#     abbreviation = models.CharField(max_length=3)
#     name = models.CharField(max_length=10)

#     def __str__(self):
#         return self.name


class Task_Type(models.Model):
    short_name = models.CharField(max_length=40)
    long_name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    chart_color = models.CharField(max_length=6)

    def __str__(self):
        return self.short_name


class Task(models.Model):
    days = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]
    # task_type = models.ForeignKey(
    #     Task_Type, on_delete=models.CASCADE, null=True, blank=True
    # )
    task_text = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    # exhibit = models.ForeignKey(
    #     Exhibit, on_delete=models.CASCADE, null=True, blank=True
    # )
    start_time = models.TimeField()
    end_time = models.TimeField()
    weekday = models.CharField(max_length=10, choices=days, default="Monday")
    start_date = None
    end_date = None

    def __str__(self):
        return f"{self.location} {self.task_text} {self.weekday} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
