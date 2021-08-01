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
                    GROUP BY date_trunc('day', time)"""

    connection = next(get_session()).connection()
    try:
        rec = connection.execute(query_text)
    finally:
        connection.close()

    x = []
    y = []
    for i in rec:
        x.append(i["date_trunc"].strftime("%d.%m"))
        y.append(i["sum"])

    lineplot(x, y, x_label="Объем, мл.", y_label="Дата", title="Объемы питания")

    pic = f"./eat_{datetime.datetime.now()}.jpg"
    plt.savefig(fname=pic)

    return pic
