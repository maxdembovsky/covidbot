import matplotlib.pyplot as plt
import requests

url = f"https://pomber.github.io/covid19/timeseries.json"


def world_stat():
    """Get and show stats of the world from json. Return date, confirmed, deaths, recovered. Create world_plot.png."""

    data = requests.get(url).json()
    date = list()

    for day_data in data['Russia']:  # create a list of dates
        date.append(day_data['date'][5:])

    confirmed, deaths, recovered = list(range(len(date))), list(range(len(date))), list(range(len(date)))
    for key, value in data.items():
        for i in range(len(value)):
            country_data = value[i]

            confirmed_ = country_data['confirmed']
            deaths_ = country_data['deaths']
            recovered_ = country_data['recovered']

            confirmed[i] += confirmed_
            deaths[i] += deaths_
            recovered[i] += recovered_

    plt.plot(date, confirmed, color='red', label='confirmed')
    plt.plot(date, deaths, color='black', label='deaths')
    plt.plot(date, recovered, color='green', label='recovered')
    plt.title("World statistics", color='purple', fontsize=14)
    plt.xlabel('Date', color='blue')
    plt.ylabel('People', color='blue')
    plt.xticks(range(0, len(date), 7))
    plt.tick_params(axis='y', labelsize=7)
    plt.tick_params(axis='x', labelsize=10)
    plt.grid(color='grey')
    plt.legend()

    plt.savefig('world_plot.png')
    plt.close()

    return date, confirmed, deaths, recovered


def world_log_scale():
    """Get and show stats of the world in a log scale. Create world_log.png."""

    date, confirmed, deaths, recovered = world_stat()

    plt.semilogy(date, confirmed, color='red', label='confirmed')
    plt.semilogy(date, deaths, color='black', label='deaths')
    plt.semilogy(date, recovered, color='green', label='recovered')
    plt.title("Logarithmic scale (World)", color='purple', fontsize=14)
    plt.xlabel('Date', color='blue')
    plt.ylabel('People', color='blue')
    plt.xticks(range(0, len(date), 7))
    plt.tick_params(axis='y', labelsize=7)
    plt.tick_params(axis='x', labelsize=10)
    plt.grid(color='grey')
    plt.legend()

    plt.savefig('world_log.png')
    plt.close()


def world_dynamics():
    """Get and show dynamics of the world. Create world_dynamics.png."""

    date, confirmed, deaths, recovered = world_stat()
    new_confirmed, new_deaths, new_recovered = list(), list(), list()

    for day in range(1, len(confirmed)):
        new_confirmed.append(confirmed[day] - confirmed[day - 1])
        new_deaths.append(deaths[day] - deaths[day - 1])
        new_recovered.append(recovered[day] - recovered[day - 1])

    del date[0]   # to make the number of variables equal

    fig, axes = plt.subplots()
    axes.bar(date, new_confirmed, color='red')
    plt.title("Dynamics (World)", color='purple', fontsize=14)
    plt.xlabel('Date', color='blue')
    plt.ylabel('People', color='blue')
    plt.xticks(range(0, len(date), 7))
    plt.tick_params(axis='y', labelsize=7)
    plt.tick_params(axis='x', labelsize=10)
    plt.grid(color='grey')
    plt.legend()

    plt.savefig('world_dynamics.png')
    plt.close()


def country_stat(country):
    """Get stats of country. Return date, confirmed, deaths, recovered."""

    data = requests.get(url).json()
    country_data = data[country]
    date, confirmed, deaths, recovered = list(), list(), list(), list()

    for data_ in country_data:
        date.append(data_['date'][5:])
        confirmed.append(data_['confirmed'])
        deaths.append(data_['deaths'])
        recovered.append(data_['recovered'])

    return date, confirmed, deaths, recovered


def stats_for_all_countries():
    """Get stats for all countries and return that information"""

    data = requests.get(url).json()
    with open('info_countries', 'w') as f:
        for key, value in data.items():
            for _ in range(1):
                confirmed = str(value[-1]['confirmed'])
                deaths = str(value[-1]['deaths'])
                recovered = str(value[-1]['recovered'])
                f.write(key + ' ' + confirmed + ' ' + deaths + ' ' + recovered + '\n')
    f.close()


def show_country_stat(country):
    """Get and show stats of country. Create country_plot.png."""

    date, confirmed, deaths, recovered = country_stat(country)

    plt.plot(date, confirmed, color='red', label='confirmed')
    plt.plot(date, deaths, color='black', label='deaths')
    plt.plot(date, recovered, color='green', label='recovered')
    plt.title("Statistics in {}".format(country), color='purple', fontsize=14)
    plt.xlabel('Date', color='blue')
    plt.ylabel('People', color='blue')
    plt.xticks(range(0, len(date), 7))
    plt.tick_params(axis='y', labelsize=7)
    plt.tick_params(axis='x', labelsize=10)
    plt.grid(color='grey')
    plt.legend()

    plt.savefig('country_plot.png')
    plt.close()


def show_log_scale_country(country):
    """Get and show stats of country in a log scale. Create country_log.png."""

    date, confirmed, deaths, recovered = country_stat(country)

    plt.semilogy(date, confirmed, color='red', label='confirmed')
    plt.semilogy(date, deaths, color='black', label='deaths')
    plt.semilogy(date, recovered, color='green', label='recovered')
    plt.title("Logarithmic scale ({})".format(country), color='purple', fontsize=14)
    plt.xlabel('Date', color='blue')
    plt.ylabel('People', color='blue')
    plt.xticks(range(0, len(date), 7))
    plt.tick_params(axis='y', labelsize=7)
    plt.tick_params(axis='x', labelsize=10)
    plt.grid(color='grey')
    plt.legend()

    plt.savefig('country_log.png')
    plt.close()


def show_dynamics_country(country):
    """Get and show dynamics of country. Create country_dynamics.png."""

    date, confirmed, deaths, recovered = country_stat(country)
    new_confirmed, new_deaths, new_recovered = list(), list(), list()

    for day in range(1, len(confirmed)):
        new_confirmed.append(confirmed[day] - confirmed[day-1])
        new_deaths.append(deaths[day] - deaths[day-1])
        new_recovered.append(recovered[day] - recovered[day-1])

    del date[0]  # to make the number of variables equal

    fig, axes = plt.subplots()
    axes.bar(date, new_confirmed, color='red')
    plt.title("Dynamics ({})".format(country), color='purple', fontsize=14)
    plt.xlabel('Date', color='blue')
    plt.ylabel('People', color='blue')
    plt.xticks(range(0, len(date), 7))
    plt.tick_params(axis='y', labelsize=7)
    plt.tick_params(axis='x', labelsize=10)
    plt.grid(color='grey')

    plt.savefig('country_dynamics.png')
    plt.close()
