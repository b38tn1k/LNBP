import json
import io
import re
from collections import defaultdict
from datetime import datetime
from dateutil import parser
import dateutil
import re
import csv


def is_date_like(s):
    # Use regular expressions to identify date-like strings
    # This is just a very basic example; actual logic too boring to do
    return any(char.isdigit() for char in s)


def combine_dates(dates):
    today = datetime.now()
    combined_date = datetime(today.year, today.month, today.day, 0, 0)
    for date_str in dates:
        try:
            if "/" in date_str:
                parsed_date = datetime.strptime(date_str, "%m/%d")
                new_year = combined_date.year
                # Adjust day to avoid 'day is out of range for month' error
                new_day = min(
                    parsed_date.day,
                    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][
                        parsed_date.month - 1
                    ],
                )
                combined_date = datetime(
                    new_year,
                    parsed_date.month,
                    new_day,
                    combined_date.hour,
                    combined_date.minute,
                )
            elif ":" in date_str:
                parsed_date = datetime.strptime(date_str, "%H:%M")
                combined_date = datetime(
                    combined_date.year,
                    combined_date.month,
                    combined_date.day,
                    parsed_date.hour,
                    parsed_date.minute,
                )
        except Exception as e:
            print(f"Error parsing date string '{date_str}': {e}")
            continue

    return combined_date


def special_char_sort(s):
    special_chars_order = {"/": 1, "\\": 2, ":": 3, ";": 4, ",": 5, "|": 6, "-": 6}
    # Extract special characters from the string using a regular expression
    special_chars = re.findall(r"[\/\\:;,\|-]", s)
    # Use the sum of the custom orders as the key for sorting
    return sum(special_chars_order.get(char, 0) for char in special_chars)


def csv_wizard_time(group):
    shape = group_outline(group)

    # Determine the shape of the data
    shape = "wide" if shape["max_col"] > shape["max_row"] else "tall"

    # Initialize the groups dictionary
    groups = {}

    td_regex = r'<td data-row="(\d+)" data-col="(\d+)" class="[^"]*">([^<]*)</td>'
    for match in re.finditer(td_regex, group):
        row, col, data = int(match.group(1)), int(match.group(2)), match.group(3)
        key = col if shape == "wide" else row
        groups.setdefault(key, set()).add(data)

    # Build group_list
    group_list = [list(val) for val in groups.values()]
    group_list = [sorted(sublist, key=special_char_sort) for sublist in group_list]

    # Fill in empty or whitespace-only values
    for i, gr in enumerate(group_list):
        for j, v in enumerate(gr):
            if not v or v.isspace():
                group_list[i][j] = group_list[i - 1][j]

    dates = []
    for group in group_list:
        date_likes = [s for s in group if is_date_like(s)]
        if date_likes:
            combined_date = combine_dates(date_likes)
            dates.append(combined_date)
            # print(f"Group: {group}, Combined Date: {combined_date}")
    return shape, dates


def group_outline(data):
    max_row, max_col = -1, -1
    min_row, min_col = 1000000, 1000000
    td_regex = r'<td data-row="(\d+)" data-col="(\d+)" class="[^"]*">([^<]*)</td>'
    # Find max_row and max_col
    for match in re.finditer(td_regex, data):
        row, col = int(match.group(1)), int(match.group(2))
        max_row, max_col = max(max_row, row), max(max_col, col)
        min_row, min_col = min(min_row, row), min(min_col, col)
    return {
        "min_row": min_row,
        "min_col": min_col,
        "max_row": max_row,
        "max_col": max_col,
    }


def convert_availability(a, t_dict):
    # t_dict has keys for the strings that match "available-marker","unavailable-marker" and "low-preference-marker"
    pass

def get_marker_strings_from_csv(my_csv, t_dict):
    csvfile = io.StringIO(my_csv)
    reader = csv.reader(csvfile, delimiter=",")

    # Initialize the dictionary to store marker strings
    marker_strings = {
        "available-marker": "",
        "unavailable-marker": "",
        "low-preference-marker": ""
    }

    # Iterate through the CSV to find marker strings
    for row_index, row in enumerate(reader):
        for key in marker_strings.keys():
            marker_info = t_dict.get(key)
            if marker_info:
                marker_row = marker_info['row']
                marker_col = marker_info['col']
                if row_index == marker_row:
                    marker_strings[key] = row[marker_col]

    return marker_strings


def wide_get_players_and_availability(target_flight, my_csv, t_dict):
    player_start_col = t_dict["player"][0]["min_col"]
    player_end_col = t_dict["player"][0]["max_col"]
    player_top_row = target_flight["min_row"]
    player_bottom_row = target_flight["max_row"]

    availability_start_col = t_dict["availability"][0]["min_col"]
    availability_end_col = t_dict["availability"][0]["max_col"]

    csvfile = io.StringIO(my_csv)
    reader = csv.reader(csvfile, delimiter=",")

    # Get marker strings from t_dict
    ms = get_marker_strings_from_csv(my_csv, t_dict)
    available_marker = ms.get("available-marker", "")
    unavailable_marker = ms.get("unavailable-marker", "")
    low_preference_marker = ms.get("low-preference-marker", "")

    # print(available_marker, low_preference_marker, unavailable_marker)
    # {'row': 2, 'col': 1, 'class': 'table-success table-info'} {'row': 3, 'col': 2, 'class': 'table-success table-warning'} {'row': 5, 'col': 3, 'class': 'table-success table-danger'}
    # the dictionary just contains the location of the markers strings in the csv. we need to use these locations with the csv to retrieve tha actual marrtker strings. just give me this bit
    players = []
    for row_index, row in enumerate(reader):
        # Check if the current row is within the desired range for players
        if player_top_row <= row_index <= player_bottom_row:
            # Extract the cells for player names
            player_names = row[player_start_col : player_end_col + 1]
            # Extract the cells for availability
            availability = row[availability_start_col : availability_end_col + 1]

            # Convert availability based on markers
            converted_availability = [
                1 if cell == available_marker else
                2 if cell == low_preference_marker else
                3 if cell == unavailable_marker else
                1  # Default to 1 (available) if none of the markers match
                for cell in availability
            ]

            player_info = {
                "names": player_names,
                "availability": converted_availability
            }
            players.append(player_info)
    return players

def extract_html_attributes(html_string):
    # Regular expression pattern to find attributes and their values
    attr_pattern = r'(\w+)=["\']([^"\']+)["\']'

    # Find all matches in the HTML string
    matches = re.findall(attr_pattern, html_string)

    # Convert matches to a dictionary
    attributes = {attr: value for attr, value in matches}
    
    # Convert numerical values to integers
    for key, value in attributes.items():
        if value.isdigit():
            attributes[key] = int(value)

    return attributes


def league_wizard_csv_to_dicts(data):
    t_dict = {}
    for k in ["flight", "availability", "player", "available-marker","unavailable-marker","low-preference-marker"]:
        t_dict[k] = []
    # first pass, grab the shape, the csv table, and the times (just because)
    for d in data:
        if "type" in d:
            if d["type"] == "time":
                shape, timeslots = csv_wizard_time(d["data"])
                t_dict["time"] = {}
                t_dict["time"]["slots"] = timeslots
                t_dict["time"]["shape"] = group_outline(d["data"])
                t_dict["time"]["example"] = d["data"]
            if d["type"] == "tableCSV":
                t_dict["csv"] = d["data"]
            if d["type"] in [
                "flight",
                "availability",
                "player",
            ]:
                t_dict[d["type"]].append(group_outline(d["data"]))
            if d["type"] in [
                "available-marker",
                "unavailable-marker",
                "low-preference-marker",
            ]:
                t_dict[d["type"]] = (extract_html_attributes(d["data"]))
                print(t_dict[d['type']])
                
    league = []
    if shape == "wide":
        for f in t_dict["flight"]:
            flight = {}
            flight["timeslots"] = t_dict["time"]["slots"]
            flight["players"] = wide_get_players_and_availability(
                f, t_dict["csv"], t_dict
            )
            league.append(flight)
    print(league)
    return league
