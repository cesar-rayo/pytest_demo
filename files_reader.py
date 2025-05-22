import csv
import json
from statistics import mean, median


def csv_reader(file_path):
    with open(file_path, "r") as csv_file:
        data = [line for line in csv.DictReader(csv_file)]
        for row in data:
            try:
                row['Lat'] = float(row['Lat'])
                row['Long'] = float(row['Long'])
                row['Altitude'] = float(row['Altitude'])
            except Exception as exp:
                raise ValueError(str(exp))
        return data


def json_reader(file_location):
    with open(file_location) as f:
        return json.load(f)


def altitude_stat_per_country(data, country, stat):
    country_altitude_list = []
    for row in data:
        if row['Country'] == country:
            country_altitude_list.append(row['Altitude'])
    if stat.lower() == 'mean':
        result = mean(country_altitude_list)
    elif stat.lower() == 'median':
        result = median(country_altitude_list)
    return {
        'Country': country,
        stat: round(result, 2)
    }


def csv_writer(row_data, output_location):
    fieldnames = row_data.keys()
    writer = csv.DictWriter(output_location, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(row_data)
    # return csv.readlines()
