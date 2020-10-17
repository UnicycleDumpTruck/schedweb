import datetime

# from datetime import date, datetime, timedelta

from tablib import Dataset
from polls.resources import TaskResource

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from plotly.offline import plot
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

from .models import Question, Task, Task_Type

# axes_ranges = {'Monday': ()}


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    # output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def time_to_date(input_time):
    return datetime.datetime.combine(datetime.date(2020, 1, 1), input_time)


def prep_df(day_of_week):
    task_list = Task.objects.filter(weekday=day_of_week)
    no_virex = task_list.exclude(task_text="Virex Spray Everything")
    q = no_virex.values(
        "location",
        "start_time",
        "end_time",
        "task_text",
        "task_type",
        "task_type__chart_color",
        "task_type__short_name",
        "task_type__long_name",
        "weekday",
        "exhibit",
        "exhibit__long_name",
    )

    df = pd.DataFrame.from_records(q)
    df["start_date"] = df.start_time.apply(time_to_date)
    df["end_date"] = df.end_time.apply(time_to_date)
    df["start_string"] = df.start_time.apply(lambda x: x.strftime("%H:%M"))
    df["end_string"] = df.end_time.apply(lambda x: x.strftime("%H:%M"))
    df["caption"] = (
        df["start_string"]
        + " to "
        + df["end_string"]
        + "<br>"
        + df["location"]
        + "<br>"
        + df["task_text"].replace("Disinfect & Prop Swap", "Disinfect<br>& Prop Swap")
    )
    df["class"] = df.task_text.apply(lambda r: task_classes.get(r, "unknown"))
    return df


def plot_day(day_of_week):
    df = prep_df(day_of_week)

    if len(df):
        fig = px.timeline(
            df,
            x_start="start_date",  # StartDate
            x_end="end_date",  # EndDate
            y="location",
            color="task_text",
            text="caption",
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(autorange=True)
        # fig.update_xaxes(range=)

        fig.update_layout(
            title=day_of_week,
            xaxis_tickformat="%-I:%M",
            font_color="blue",
            font_size=10,
            title_font_family="Arial",
            title_font_color="blue",
            # legend_title_font_color="green",
            showlegend=False,
            yaxis_title="",
            xaxis_title="",
        )
        fig.update_xaxes(tick0=0.25)
        config = {"displayModeBar": False}

    plot_div = plot(
        fig,
        output_type="div",
        config=config,
    )
    return plot_div


def wednesday(request):
    template = loader.get_template("polls/tasks.html")
    context = {"plot_div": plot_day("Wednesday")}
    return HttpResponse(template.render(context, request))


def tasks(request):
    template = loader.get_template("polls/tasks.html")
    divs = "<br>".join(
        [
            plot_day("Monday"),
            plot_day("Tuesday"),
            plot_day("Wednesday"),
            plot_day("Thursday"),
            plot_day("Friday"),
            plot_day("Weekend"),
        ]
    )
    context = {"plot_div": divs}
    return HttpResponse(template.render(context, request))


def simple_upload(request):
    if request.method == "POST":
        person_resource = TaskResource()
        dataset = Dataset()
        new_persons = request.FILES["myfile"]

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(
            dataset, dry_run=True
        )  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, "core/simple_upload.html")


def per_delta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
    # usage: for result in per_delta(datetime.datetime.now(), datetime.datetime.now().replace(hour=19))


def list_of_times(start, end, delta):
    return list(result.strftime("%H:%M") for result in per_delta(start, end, delta))


def day_of_times():
    return list_of_times(
        datetime.datetime(2020, 1, 1, 0, 0, 0, 0),
        datetime.datetime(2020, 1, 1, 23, 59, 59, 0),
        datetime.timedelta(minutes=15),
    )


task_rows = {
    "Learn & Play": 2,
    "Disinfect & Prop Swap": 3,
    "Wipe down": 4,
    "Prop Swap": 3,
    "Prop Swap Only": 3,
}


task_classes = {
    "Learn & Play": "learn_and_play",
    "Disinfect & Prop Swap": "spray_and_swap",
    "Wipe down": "wipe_down",
    "Prop Swap": "prop_swap",
    "Prop Swap Only": "prop_swap",
}


def grid(request):
    template = loader.get_template("polls/grid.html")
    time_list = list_of_times(
        datetime.datetime(2020, 1, 1, 8, 45, 0, 0),
        datetime.datetime(2020, 1, 1, 16, 0, 0, 0),
        datetime.timedelta(minutes=15),
    )
    wed_df = prep_df("Wednesday")
    wed_df["start_col"] = wed_df.start_date.apply(
        lambda x: time_list.index(x.strftime("%H:%M")) + 1
    )
    wed_df["end_col"] = wed_df.end_date.apply(
        lambda x: time_list.index(x.strftime("%H:%M")) + 1
    )
    wed_df["row"] = wed_df.task_text.apply(lambda r: task_rows.get(r, 6))
    wed_events = wed_df.to_dict("index").values()

    context = {
        "num_columns": len(time_list),
        "col_width": (100 / (len(time_list))),
        "wed_events": wed_events,
        "time_list": enumerate(time_list, 1),
    }
    return HttpResponse(template.render(context, request))


def vgrid(request):
    template = loader.get_template("polls/vgrid.html")
    time_list = list_of_times(
        datetime.datetime(2020, 1, 1, 9, 0, 0, 0),
        datetime.datetime(2020, 1, 1, 16, 0, 0, 0),
        datetime.timedelta(minutes=15),
    )
    hour_rows = [
        (index, time) for (index, time) in enumerate(time_list, 1) if time[2:] == ":00"
    ]
    # for index, time in time_list:
    #     if time[2:4] == ":00":

    df = prep_df("Thursday")
    df["start_row"] = df.start_date.apply(
        lambda x: time_list.index(x.strftime("%H:%M")) + 1
    )
    df["end_row"] = df.end_date.apply(
        lambda x: time_list.index(x.strftime("%H:%M")) + 1
    )
    df["row"] = df.task_text.apply(lambda r: task_rows.get(r, 6))
    events = df.to_dict("index").values()
    # print(f"{events=}")
    print(f"{hour_rows=}")
    print(f"{time_list=}")
    context = {
        "num_rows": len(time_list),
        # "col_width": (100 / (len(time_list))),
        "events": events,
        "time_list": enumerate(time_list, 1),
        "hour_rows": hour_rows,
    }
    return HttpResponse(template.render(context, request))
