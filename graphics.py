import matplotlib.pyplot as plt
import datetime
from repository import get_session


def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw=2, color='#539caf', alpha=1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


def get_eat_graphic():
    query_text = """
                    SELECT date_trunc('day', time), SUM(value) FROM events
                    WHERE events.type='eat' and events.value > 0
                    GROUP BY date_trunc('day', time)
                    ORDER BY date_trunc('day', time) ASC"""

    connection = get_session().connection()
    rec = connection.execute(query_text)

    x = []
    y = []
    for i in rec:
        x.append(i["date_trunc"].strftime("%d.%m"))
        y.append(i["sum"])

    lineplot(x, y, y_label="Объем, мл.", x_label="Дата", title="Объемы питания")

    pic = f"./eat_{datetime.datetime.now()}.jpg"
    plt.savefig(fname=pic)

    return pic

def get_():
    query_text = """
                SELECT 
                  date_part('hour', time) AS "hour_number",
                  AVG(events.value) AS "value",
                  AVG(CurrentDay.value) AS "current_day_value"
                FROM 
                  events 
                  LEFT JOIN (
                  SELECT 
                      date_part('hour', time) AS "hour_number",
                      AVG(value) AS "value"
                    FROM 
                        events
                    WHERE 
                      events.type='eat' 
                      and events.value > 0
                      AND events.time >= date_trunc('day', current_timestamp)
                    GROUP BY 
                      date_part('hour', time)
                    ORDER BY 
                      date_part('hour', time) ASC
                    ) AS CurrentDay on date_part('hour', events.time) = CurrentDay.hour_number
                WHERE 
                  events.type='eat' 
                  and events.value > 0
                GROUP BY 
                  date_part('hour', time)
                ORDER BY 
                  date_part('hour', time) ASC
                  """