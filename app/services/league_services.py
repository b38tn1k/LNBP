import json
import io
import re
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser
import dateutil
import re
import csv


def is_date_like(s):
    # Use regular expressions to identify date-like strings
    # This is just a very basic example; actual logic too boring to do
    """
    This function checks if a given string is date-like by checking if it contains
    any digits.

    Args:
        s (str): In the `is_date_like` function , the `s` input parameter is the
            string that we want to check if it looks like a date or not.

    Returns:
        bool: The output returned by the function `is_date_like()` would be `True`
        if the input string contains at least one digit.

    """
    return any(char.isdigit() for char in s)


def combine_dates(dates):
    """
    This function combines multiple date strings into a single datetime object
    using the current time as the basis for the combined date.

    Args:
        dates (list): The `dates` input parameter is a list of date strings that
            are processed and combined into a single datetime object using the
            methods you provided.

    Returns:
        str: The output returned by this function is a `datetime` object representing
        the combined date and time.

    """
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
    """
    This function sorts a string based on the frequency of special characters ("/",
    "\", ":", ";", "," , "|" and "-") present inside the string.

    Args:
        s (str): The `s` input parameter is the string that needs to be sorted
            based on the special characters it contains.

    Returns:
        int: The output returned by this function is the sorted list of special
        characters extracted from the input string.

    """
    special_chars_order = {"/": 1, "\\": 2, ":": 3, ";": 4, ",": 5, "|": 6, "-": 6}
    # Extract special characters from the string using a regular expression
    special_chars = re.findall(r"[\/\\:;,\|-]", s)
    # Use the sum of the custom orders as the key for sorting
    return sum(special_chars_order.get(char, 0) for char in special_chars)


def csv_wizard_time(group):
    """
    This function takes a group of rows from a HTML table and extracts the date
    information from it. It first determines the shape of the data (wide or tall)
    and then uses regular expressions to identify and group together contiguous
    cells that contain dates.

    Args:
        group (str): The `group` input parameter is a string containing the content
            of a table row.

    Returns:
        list: Based on the given code snippet; the output returned by `csv_wizard_time`
        function is two values -
        
        1/ 'shape', a string indicating either "tall" or "wide" based on the max
        col and row lengths of the provided group's CSV data
        2/ 'dates', a list of combined date strings extracted from the 'date-like'
        cells within the provided group.

    """
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
            dates.append(combined_date.isoformat())
            # print(f"Group: {group}, Combined Date: {combined_date}")
    return shape, dates


def group_outline(data):
    """
    This function extracts the maximum and minimum row and column numbers from a
    given table data using regular expressions.

    Args:
        data (str): The `data` input parameter is the HTML content that contains
            the tables with columns and rows to be processed by the function.

    Returns:
        dict: The output returned by this function is a dictionary with four
        key-value pairs:
        
        {
        "min_row": 1000000 (the minimum row number),
        "min_col": 1000000 (the minimum column number),
        "max_row": -1 (the maximum row number),
        "max_col": -1 (the maximum column number)
        }

    """
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


def get_marker_strings_from_csv(my_csv, t_dict):
    """
    This function takes a CSV string and a dictionary of marker information and
    returns a dictionary of marker strings based on the row indices and column
    headers from the CSV.

    Args:
        my_csv (str): The `my_csv` input parameter is a string that contains the
            contents of a CSV file.
        t_dict (dict): The `t_dict` input parameter is a dictionary that contains
            information about each marker type (e.g., "available-marker",
            "unavailable-marker", "low-preference-marker").

    Returns:
        dict: The output returned by this function is a dictionary with marker
        strings for each marker type: {"available-marker": "<insert available
        marker string here>", "unavailable-marker": "<insert unavailable marker
        string here>", "low-preference-marker": "<insert low preference marker
        string here>"}

    """
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
    """
    This function `wide_get_players_and_availability` reads a CSV file and returns
    a list of player information dictionaries where each dictionary has the player
    names and their availability status (available or not available). The function
    takes three input arguments:
    1/ `target_flight`: A dict containing information about the flight (min/max
    row & col for players and availability)
    2/ `my_csv`: The CSV file to read
    3/ `t_dict`: A dict of marker strings to their locations (rows and columns)
    within the CSV file.
    The function first extracts the rows and columns of interest from `target_flight`,
    then reads the entire CSV file into a stringIO object and passes it to the
    `csv` module to create a reader object. It then uses the marker strings found
    at the start and end of each row (stored as dict values under `t_dict["player"]`
    and `t_dict["availability"]`) to extract only those rows with player or
    availability data within the desired range specified by `target_flight`. Finally
    it iterates over each matching row of the CSV file using list comprehensions
    to create a dictionary for each player name (retrieved from a portion of that
    row) that contains information about their availability status (determined
    based on presence of special markers).

    Args:
        target_flight (dict): The `target_flight` input parameter specifies the
            range of rows to consider when checking for player availability and
            extracting their names and availability information from the CSV file.
        my_csv (str): The `my_csv` input parameter is a string representing the
            contents of the CSV file to be processed.
        t_dict (dict): The `t_dict` input parameter is a dictionary that contains
            information about the structure of the CSV file being processed. It
            is used to define the columns and ranges for extracting player names
            and availability information from the CSV.

    Returns:
        dict: The output returned by the `wide_get_players_and_availability`
        function is a list of player information objects `{ "names": [<list of
        player names>], "availability": [<list of availability values (1 for
        available/unavailable)"] }` for each row within the desired range for players.

    """
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
    """
    This function takes an HTML string as input and extracts all attribute-value
    pairs found within it.

    Args:
        html_string (str): The `html_string` input parameter is the HTML content
            from which we want to extract the attributes and their values.

    Returns:
        dict: The output returned by this function is a dictionary containing the
        attributes found within the given HTML string as key-value pairs.

    """
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
    """
    This function takes a list of dictionaries representing CSV data for a fantasy
    football league schedule and returns a list of dictionaries representing the
    league data with the following structure:
    	- Each dictionary represents one flight (time slot)
    	+ "timeslots": A list of time slots available during the flight
    	+ "players": A list of player availability information for each player during
    the flight
    The function performs the following operations:
    1/ First pass: Extract shape (wide or not), CSV table data and timeslots from
    the first line of the input data
    2/ Define dictionaries for each type of data: "time", "csv" and for the types
    of markers ("available-marker", "unavailable-marker", "low-preference-marker")
    3/ For each input dictionary:
    	a. Check if it contains "type" and if it's one of the supported types
    	b.

    Args:
        data (dict): The `data` input parameter is a list of dictionaries representing
            CSV data. It is passed as an argument to the function and is used as
            the input for the function's operations.

    Returns:
        dict: Based on the code provided:
        
        The output returned by this function is `league`, which is a list of
        dictionaries containing information about flights and their players' availability.

    """
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
                
    league = []
    if shape == "wide":
        for f in t_dict["flight"]:
            flight = {}
            flight["timeslots"] = t_dict["time"]["slots"]
            flight["players"] = wide_get_players_and_availability(
                f, t_dict["csv"], t_dict
            )
            league.append(flight)
    return league

def build_league_from_json(my_club, data):
    datetime_objects = [datetime.fromisoformat(iso_string) for iso_string in data['timeslots']]
    earliest_date = min(datetime_objects)
    latest_date = max(datetime_objects)
    game_duration_hours = data['game_duration'] 
    duration = timedelta(hours=game_duration_hours)
    latest_date = latest_date + duration
    my_league = my_club.create_league(data['name'], data['type'], earliest_date, latest_date, add=True, commit=False)
    
    for t in datetime_objects:
        my_league.create_timeslot(t, t + duration, add=True, commit=False)

    for flight in data['flights']:
        my_flight = my_league.create_flight(flight['name'])
        for p in flight['players_and_availabilities']:
            player = my_club.find_or_create_player(p['name'])
            my_flight.add_player(player)
            my_league.add_player(player)
            print(player)
    

    