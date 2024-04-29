#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def add_train(trains, departure_point, number_train, time_departure, destination):
    """
    Добавить данные о поезде.
    """
    trains.append(
        {
            "departure_point": departure_point,
            "number_train": number_train,
            "time_departure": time_departure,
            "destination": destination
        }
    )

    return trains


def display_trains(trains):
    """
    Отобразить список поездов со станциями.
    """
    # Проверить, что список поездов не пуст.
    if trains:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+--{}--+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 13,
            '-' * 18,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^13} | {:^18} | {:^14} |'.format(
                "№",
                "Пункт отправления",
                "Номер поезда",
                "Время отправления",
                "Пункт назначения"
            )
        )
        print(line)

        # Вывести данные о всех поездах со станциями.
        for idx, train in enumerate(trains, 1):
            print(
                '| {:>4} | {:<30} | {:<13} | {:>18} | {:^16} |'.format(
                    idx, train.get('departure_point', ''),
                    train.get('number_train', ''),
                    train.get('time_departure', ''),
                    train.get('destination', '')
                )
            )
            print(line)

    else:
        print("Список поездов пуст.")


def select_trains(trains, point_user):
    """
    Выбрать поезда по пункту назначения.
    """
    # Сформировать список поездов.
    result = []
    for train in trains:
        if point_user == str.lower(train['destination']):
            result.append(train)

    # Возвратить список выбранных поездов, направляющихся в пункт.
    return result


def save_trains(file_name, trains):
    """
    Сохранить все поезда со станциями в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(trains, fout, ensure_ascii=False, indent=4)


def load_trains(file_name):
    """
    Загрузить все поезда со станциями из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("trains")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления поезда.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new train"
    )
    add.add_argument(
        "-dep",
        "--departure_point",
        action="store",
        required=True,
        help="The train's departure point"
    )
    add.add_argument(
        "-n",
        "--number_train",
        action="store",
        required=True,
        help="The train's number"
    )
    add.add_argument(
        "-t",
        "--time_departure",
        action="store",
        required=True,
        help="The time departure of train"
    )
    add.add_argument(
        "-des",
        "--destination",
        action="store",
        required=True,
        help="The destination of train"
    )

    # Создать субпарсер для отображения всех поездов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all trains"
    )

    # Создать субпарсер для выбора поездов по пунктам назначения.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the trains"
    )
    select.add_argument(
        "-P",
        "--point_user",
        action="store",
        required=True,
        help="The required point"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить все поезда со станциями из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        trains = load_trains(args.filename)
    else:
        trains = []

    # Добавить поезд со станциями.
    if args.command == "add":
        trains = add_train(
            trains,
            args.departure_point,
            args.number_train,
            args.time_departure,
            args.destination
        )
        is_dirty = True

    # Отобразить все поезда со станциями.
    elif args.command == "display":
        display_trains(trains)

    # Выбрать требуемые поезда.
    elif args.command == "select":
        selected = select_trains(trains, args.point_user)
        display_trains(selected)

    # Сохранить данные в файл, если список поездов был изменен.
    if is_dirty:
        save_trains(args.filename, trains)


if __name__ == "__main__":
    main()
