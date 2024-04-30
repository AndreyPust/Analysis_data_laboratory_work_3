#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bisect
import json
import os
import sys
import click


def add_train(trains, departure_point, number_train, time_departure, destination):
    """
    Добавить данные о поездах со станциями.
    """
    is_dirty = False
    train = {
        "departure_point": departure_point,
        "number_train": number_train,
        "time_departure": time_departure,
        "destination": destination
    }
    if train not in trains:
        bisect.insort(
            trains,
            train,
            key=lambda item: item.get("time_departure"),
        )
        is_dirty = True
    else:
        click.echo("Данный поезд уже добавлен.")
    return trains, is_dirty


def display_trains(trains):
    """
    Отобразить список поездов со станциями.
    """
    if trains:
        line = '+-{}-+-{}-+-{}-+-{}-+--{}--+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 13,
            '-' * 18,
            '-' * 14
        )
        click.echo(line)
        click.echo(
            '| {:^4} | {:^30} | {:^13} | {:^18} | {:^14} |'.format(
                "№",
                "Пункт отправления",
                "Номер поезда",
                "Время отправления",
                "Пункт назначения"
            )
        )
        click.echo(line)
        for idx, train in trains:
            click.echo(
                '| {:>4} | {:<30} | {:<13} | {:>18} | {:^16} |'.format(
                    idx, train.get('departure_point', ''),
                    train.get('number_train', ''),
                    train.get('time_departure', ''),
                    train.get('destination', '')
                )
            )
        click.echo(line)
    else:
        click.echo("Список поездов пуст.")


def select_trains(trains, point_user):
    """
    Выбрать поезда по пункту назначения.
    """
    selected = []
    for train in trains:
        if point_user == str.lower(train['destination']):
            selected.append(train)

    # Возвратить список выбранных поездов, направляющихся в пункт.
    return selected


def save_trains(file_name, trains):
    """
    Сохранить все поезда в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w") as file_out:
        # Записать данные из словаря в формат JSON и сохранить их
        # в открытый файл.
        json.dump(trains, file_out, ensure_ascii=False, indent=4)


def load_trains(file_name):
    """
    Загрузить все поезда из файла JSON.
    """
    # Открыть файл с заданным именем и прочитать его содержимое.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.group()
def command():
    pass


@command.command()
@click.argument("filename")
@click.option("-dep", "--departure_point", required=True, help="The departure point train")
@click.option("-n", "--number_train", required=True, help="The number train")
@click.option("-t", "--time_departure", required=True, help="The time departure of train")
@click.option("-des", "--destination", required=True, help="The destination of train")
def add(filename, departure_point, number_train, time_departure, destination):
    """
    Add a new train.
    """

    filename = os.path.join("data", filename)
    trains = load_trains(filename)

    routes, is_dirty = add_train(trains, departure_point.lower(), number_train.lower(), time_departure.lower(), destination.lower())
    if is_dirty:
        save_trains(filename, trains)


@command.command()
@click.argument("filename")
@click.option("-p", "--point_user", required=True, help="Destination train")
def select(filename, point_user):
    """
    Select the trains
    """
    filename = os.path.join("data", filename)
    point_user = point_user.lower()
    trains = load_trains(filename)
    selected_trains = select_trains(trains, point_user)
    display_trains(selected_trains)


@command.command()
@click.argument("filename")
def display(filename):
    """
    Display all trains
    """
    filename = os.path.join("data", filename)
    trains = load_trains(filename)
    display_trains(trains)


if __name__ == "__main__":
    command()
