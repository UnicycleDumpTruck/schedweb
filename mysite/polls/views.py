import datetime

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from plotly.offline import plot
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

from .models import Question, Task, Task_Type


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


# def tasks(request):
#     latest_task_list = Task.objects.order_by("start_time")[:5]
#     output = ", ".join([t.start_time for t in latest_task_list])
#     return HttpResponse(output)


def time_to_date(input_time):
    return datetime.datetime.combine(datetime.date(2020, 1, 1), input_time)


def tasks(request):
    task_list = Task.objects.all()

    qs = Task.objects.all()
    q = qs.values(
        "start_time",
        "end_time",
        "task_type",
        "task_type__chart_color",
        "task_type__short_name",
        "task_type__long_name",
        "weekday",
        "exhibit",
    )

    # for row in q:
    #     today = datetime.datetime.today()
    #     today.replace(hour=row["start_time"].hour, minute=row["start_time"].minute)
    #     row["start_date"] = today
    #     today.replace(hour=row["end_time"].hour, minute=row["end_time"].minute)
    #     row["end_date"] = today

    # for row in q:
    #     row["start_time"] = datetime.datetime.combine(
    #         datetime.date(1, 1, 1), row["start_time"]
    #     )
    #     row["end_time"] = datetime.datetime.combine(
    #         datetime.date(1, 1, 1), row["end_time"]
    #     )

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
        + df["exhibit"]
        + "<br>"
        + df["task_type__long_name"]
    )

    # df.start_time = df.start_time.apply(time_to_date)
    # df.end_time = df.end_time.apply(time_to_date)

    if len(df):
        # print(df)
        fig = px.timeline(
            df,
            x_start="start_date",  # StartDate
            x_end="end_date",  # EndDate
            y="location",
            color="task_type__chart_color",
            text="caption",
        )
        fig.update_yaxes(autorange="reversed")

        fig.update_layout(
            title="Exhibit Cleaning",
            xaxis_tickformat="%-I:%M",
            font_color="blue",
            font_size=10,
            title_font_family="Arial",
            title_font_color="red",
            legend_title_font_color="green",
        )
        fig.update_xaxes(tick0=0.25)
        config = {"displayModeBar": False}
        # fig.show(config=config)

        # configkeys = (
        # 'editable',
        # 'autosizable',
        # 'fillFrame',
        # 'frameMargins',
        # 'scrollZoom',
        # 'doubleClick',
        # 'showTips',
        # 'showLink',
        # 'sendData',
        # 'linkText',
        # 'showSources',
        # 'displayModeBar',
        # 'modeBarButtonsToRemove',
        # 'modeBarButtonsToAdd',
        # 'modeBarButtons',
        # 'displaylogo',
        # 'plotGlPixelRatio',
        # 'setBackground',
        # 'topojsonURL')

    plot_div = plot(
        fig,
        output_type="div",
        config=config,
    )

    template = loader.get_template("polls/tasks.html")
    context = {"task_list": task_list, "task_df": df, "plot_div": plot_div}
    # output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(template.render(context, request))
    # return HttpResponse(plot_div)


dates_for_days = {
    "mon": "2020-09-08",
    "tue": "2020-09-09",
    "wed": "2020-09-10",
    "thu": "2020-09-11",
    "fri": "2020-09-12",
    "sat": "2020-09-13",
    "sun": "2020-09-14",
}


def formatDate(weekday, time_of_day):
    if len(time_of_day) == 4:
        time = f"{time_of_day[0:2]}:{time_of_day[2:]}:00"
    else:
        time = f"{time_of_day[0]}:{time_of_day[1:2]}:00"
    date = f"{dates_for_days.get(str(weekday))} {time}"
    # print(date)
    return date


def formatTime(time):
    if int(time) < 1300:
        return f"{time[0:2]}:{time[2:]}"
    else:
        return f"{int(time[0:2])-12}:{time[2:]}"


def fillDataFrame(events):
    # with open("input.csv", "r") as input_file:
    # reader = csv.DictReader(input_file)
    # events = list(reader)
    for row in events:
        row["EndDate"] = formatDate(row["Day"], row["End"])
        row["exhibit1"] = exhibits.get(row["exhibit1"])
        row["exhibit2"] = exhibits.get(row["exhibit2"])
        if row["exhibit2"]:
            row["Exhibits"] = f"{row['exhibit1']} &<br>{row['exhibit2']}"
        else:
            row["Exhibits"] = row["exhibit1"]
        row["Task"] = tasks[row["Task"]]
        row[
            "Time"
        ] = f"{row['Exhibits']}<br>{row['Task']}<br>{formatTime(row['Start'])} - {formatTime(row['End'])}"
        row["StartDate"] = formatDate(row["Day"], row["Start"])

    all_events_df = pd.DataFrame(events)


def createDataFrame(tasks):
    df = pd.createDataFrame()
    for task in tasks:
        pass


def plotSingleDay(ddf, day):
    # print(day)
    df = ddf.loc[all_events_df["weekday"] == day]
    if len(df):
        print(df)
        fig = px.timeline(
            df,
            x_start="StartDate",
            x_end="EndDate",
            y="Exhibits",
            color="Task",
            text="Time",
        )
        fig.update_yaxes(autorange="reversed")

        fig.update_layout(
            title=f"{days[day]} Exhibit Cleaning",
            xaxis_tickformat="%-I:%M",
            font_color="blue",
            font_size=10,
            title_font_family="Arial",
            title_font_color="red",
            legend_title_font_color="green",
        )
        fig.update_xaxes(tick0=0.25)
        config = {"displayModeBar": True}
        fig.show(config=config)
