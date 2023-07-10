import os
import json
import re
import itertools
from collections import defaultdict


STOP_NAME_FORMAT = r'([A-Z]\w+\s)+(Road|Avenue|Boulevard|Street)$'
STOP_TYPE_FORMAT = r'[SOF]$'
A_TIME_FORMAT = r'(((0[0-9]|1[0-9]|2[0-3]):(0[0-9]|[1-5][0-9]))|(24:00))$'
ANY_FORMAT = r'.*'


# -------------------------------------------------------
#  Data type checks
# -------------------------------------------------------
def is_integer(val):
    return type(val) is int


def is_string(val):
    return type(val) is str


def is_char(val):
    return type(val) is str and len(val) <= 1


# -------------------------------------------------------
#  Fields properties
# -------------------------------------------------------
class Field:

    def __init__(self, dtype_check, data_format, required):
        self.dtype_check = dtype_check
        self.format = data_format
        self.required = required


FIELDS = {
    'bus_id': Field(is_integer, ANY_FORMAT, True),
    'stop_id': Field(is_integer, ANY_FORMAT, True),
    'stop_name': Field(is_string, STOP_NAME_FORMAT, True),
    'next_stop': Field(is_integer, ANY_FORMAT, True),
    'stop_type': Field(is_char, STOP_TYPE_FORMAT, False),
    'a_time': Field(is_string, A_TIME_FORMAT, True),
}


# -------------------------------------------------------
#  Functions for data processing
# -------------------------------------------------------
def get_bus_stops_by_line(data):
    stops_by_line = defaultdict(dict)
    for el in data:
        stop_type = re.sub('^$', 'B', el['stop_type'])
        stops_by_line.setdefault(el['bus_id'], {'S': set(), 'F': set(), 'O': set(), 'B': set(), 'all': set()})
        stops_by_line[el['bus_id']][stop_type].add(el['stop_name'])
        stops_by_line[el['bus_id']]['all'].add(el['stop_name'])

    return stops_by_line


def get_transfer_stops(stops_by_line):
    combs = itertools.combinations([stops_by_line[line]['all'] for line in stops_by_line], 2)
    intersected = [comb[0] & comb[1] for comb in combs]
    return set().union(*intersected)


def get_bus_stops_by_type(stops_by_line):
    transfer_stops = get_transfer_stops(stops_by_line)
    start_stops = set()
    finish_stops = set()
    on_demand_stops = set()
    for line in stops_by_line:
        start_stops.update(stops_by_line[line]['S'])
        finish_stops.update(stops_by_line[line]['F'])
        on_demand_stops.update(stops_by_line[line]['O'])

    return start_stops, transfer_stops, finish_stops, on_demand_stops


# -------------------------------------------------------
#  Checks
# -------------------------------------------------------
def check_stops(data):
    stops_by_line = get_bus_stops_by_line(data)

    for line in stops_by_line:
        if len(stops_by_line[line]['S']) == 0 or len(stops_by_line[line]['F']) == 0:
            print(f'There is no start or end stop for the line: {line}.')
            return

    start_stops, transfer_stops, finish_stops, on_demand_stops = get_bus_stops_by_type(stops_by_line)
    print(f"Start stops: {len(start_stops)} {sorted(start_stops)}")
    print(f"Transfer  stops: {len(transfer_stops)} {sorted(transfer_stops)}")
    print(f"Finish  stops: {len(finish_stops)} {sorted(finish_stops)}")
    print(f"On-demand  stops: {len(on_demand_stops)} {sorted(on_demand_stops)}")


def check_on_demand_stops(data):
    stops_by_line = get_bus_stops_by_line(data)
    start_stops, transfer_stops, finish_stops, on_demand_stops = get_bus_stops_by_type(stops_by_line)
    wrong_stops = []
    for stop in on_demand_stops:
        if any(stop in other_stops for other_stops in zip(start_stops, transfer_stops, finish_stops)):
            wrong_stops.append(stop)
    print('On demand stops test:')
    if wrong_stops:
        print(f'Wrong stop type: {sorted(wrong_stops)}')
    else:
        print('OK')


def check_arrival_times(data):
    stops = defaultdict(list)
    time_errors = []
    for el in data:
        if any(err[0] == el['bus_id'] for err in time_errors):
            continue

        stops[el['bus_id']].append(el['a_time'])

        if len(stops[el['bus_id']]) >= 2 and stops[el['bus_id']][-1] <= stops[el['bus_id']][-2]:
            time_errors.append((el['bus_id'], el['stop_name']))

    print('Arrival time test:')
    if time_errors:
        for err in time_errors:
            print(f'bus_id line {err[0]}: wrong time on station {err[1]}')
    else:
        print('OK')


def check_data_types(data):
    errors = defaultdict(int)
    for el in data:
        for key in el:

            if FIELDS[key].required:
                if el[key] == '':
                    errors[key] += 1
                    continue

            errors[key] += not FIELDS[key].dtype_check(el[key])

    total_errors = sum(errors.values())
    print(f'Type and required field validation: {total_errors} errors')
    for key in errors:
        print(f'{key}: {errors[key]}')


def check_data_formats(data):
    errors = defaultdict(int)
    for el in data:
        for key in el:

            if not FIELDS[key].required and el[key] == '':
                continue

            errors[key] += (re.match(FIELDS[key].format, str(el[key])) is None)

    total_errors = sum(errors.values())
    print(f'Format validation: {total_errors} errors')
    for key in errors:
        if FIELDS[key].format != ANY_FORMAT:
            print(f'{key}: {errors[key]}')


def load_data(path_to_json_data):
    if not os.path.exists(path_to_json_data):
        return
    with open(path_to_json_data) as fp:
        data = json.load(fp)

    return data


def main():
    data = load_data(input('Enter path to JSON file:\n'))
    check_data_types(data)
    check_data_formats(data)
    check_arrival_times(data)
    check_stops(data)
    check_on_demand_stops(data)


if __name__ == '__main__':
    main()
