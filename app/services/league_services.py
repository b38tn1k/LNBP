import json
import io
import re
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser
import dateutil
import re
import csv
from app.services.scheduler import Player, GameSlot, SingleFlightScheduleTool, generateGameSlotAvailabilityScores


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
        "low-preference-marker": "",
    }

    # Iterate through the CSV to find marker strings
    for row_index, row in enumerate(reader):
        for key in marker_strings.keys():
            marker_info = t_dict.get(key)
            if marker_info:
                marker_row = marker_info["row"]
                marker_col = marker_info["col"]
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
                1
                if cell == available_marker
                else 2
                if cell == low_preference_marker
                else 3
                if cell == unavailable_marker
                else 1  # Default to 1 (available) if none of the markers match
                for cell in availability
            ]

            player_info = {
                "names": player_names,
                "availability": converted_availability,
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
    for k in [
        "flight",
        "availability",
        "player",
        "available-marker",
        "unavailable-marker",
        "low-preference-marker",
    ]:
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
                t_dict[d["type"]] = extract_html_attributes(d["data"])

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
    """
    This function builds a league from a JSON object containing data such as the
    name of the league and its type as well as the timeslots available for play
    and the duration of games played.

    Args:
        my_club (): The `my_club` parameter is used to create a new league associated
            with the provided club.
        data (dict): The `data` input parameter is a dictionary containing the
            data for building the league.

    """
    print(data)
    datetime_objects = [
        datetime.fromisoformat(iso_string) for iso_string in data["timeslots"]
    ]
    earliest_date = min(datetime_objects)
    latest_date = max(datetime_objects)
    game_duration_hours = data["game_duration"]
    duration = timedelta(hours=game_duration_hours)
    latest_date = latest_date + duration
    my_league = my_club.create_league(
        data["name"], data["type"], earliest_date, latest_date, add=True, commit=False
    )

    for t in datetime_objects:
        my_league.create_timeslot(t, t + duration, add=True, commit=False)

    for flight in data["flights"]:
        my_flight = my_league.create_flight(flight["name"])
        for p in flight["players_and_availabilities"]:
            player = my_club.find_or_create_player(p["name"])
            my_flight.add_player(player)
            my_league.add_player(player)
            for i in range(len(p["availability"])):
                player_availability = p["availability"][i]
                ts = my_league.timeslots[i]
                my_league.add_player_availability(
                    player, ts, player_availability, add=True, commit=False, force=True
                )
    return my_league


def facility_to_league(league, d):
    # {'event': 'facility_in_league', 'ids': 1, 'values': False}
    """
    This function takes a league and a dictionary `d` as inputs. It adds or removes
    a facility from the league based on the value of `d['values']`. If `d['values']`
    is True (i.e., the value is "true"), it adds the facility with the given ID
    to the league.

    Args:
        league (dict): The `league` input parameter is a reference to the League
            object that contains the facilities to be updated based on the provided
            `d` dictionary.
        d (dict): The `d` input parameter is a dictionary containing information
            about the facility to be added or removed from the league.

    """
    if d["values"] is True:
        f = league.club.get_facility_by_id(d["ids"])
        league.add_facility(f)
    else:
        league.remove_facility_by_id(d["ids"])


def update_game_duration(league, d):
    """
    This function updates the end time of each timeslot for a league by adding a
    fixed number of minutes to its start time.

    Args:
        league (dict): The `league` input parameter is a reference to an object
            that contains Timeslots for the game schedule.
        d (dict): The `d` input parameter is a dictionary containing the values
            for the game duration minutes.

    """
    new_duration_minutes = d["values"]
    for ts in league.timeslots:
        new_end_time = ts.start_time + timedelta(minutes=new_duration_minutes)
        ts.end_time = new_end_time


def update_timeslot(league, d):
    # {'event': 'timeslot', 'ids': 1, 'values': '2023-10-03T18:30:00.000'}
    """
    This function takes a dictionary `d` with the fields `'ids'` and `'values'`,
    where `'ids'` is an integer ID and `'values'` is a datetime string.

    Args:
        league (dict): The `league` input parameter is used to retrieve a timeslot
            object from the league's database based on the given ID.
        d (dict): In this function `d` is a dictionary containing information about
            the timeslot to be updated. It has one key-value pair:

                - `ids`: the ID of the timeslot to be updated (int)
                - `values`: the start time of the game as a string format
            'YYYY-MM-DDTHH:MM:SS.FFF' (e.g.

    """
    ts = league.get_timeslot_by_id(d["ids"])
    new_start_time = datetime.strptime(d["values"], "%Y-%m-%dT%H:%M:%S.%f")
    game_duration = league.get_game_duration()
    new_end_time = new_start_time + timedelta(minutes=game_duration)
    ts.start_time = new_start_time
    ts.end_time = new_end_time


def update_flight_name(league, d):
    """
    This function updates the name of a flight with the specified ID (retrieved
    from the league) to the given name provided as input.

    Args:
        league (): The `league` input parameter is a reference to the parent League
            object that contains the flight to be updated.
        d (dict): The `d` input parameter is a dictionary that contains the values
            for the flight name to be updated.

    """
    f = league.get_flight_by_id(d["ids"])
    f.name = d["values"]


def add_player_to_league(league, d):
    """
    This function adds a player to a league. It first retrieves the player and
    flight objects based on the IDs provided and then adds the player to the flight
    and the league.

    Args:
        league (): The `league` input parameter is used to pass the `League` object
            as a parameter to the function.
        d (dict): The `d` parameter is a dictionary containing information about
            the player to be added to the league.

    """
    flight = league.get_flight_by_id(d["ids"]["flight"])
    player = league.club.get_player_by_id(d["ids"]["player"])
    print(player, type(player))
    if player is not None:
        flight.add_player(player)
        league.add_player(player)
        for i in range(len(league.timeslots)):
            player_availability = 1
            ts = league.timeslots[i]
            league.add_player_availability(
                player, ts, player_availability, add=True, commit=False, force=True
            )


def update_league_rules(league, d):
    """
    This function updates a league's rules based on the contents of a dictionary
    'd', which contains key-value pairs representing different rule settings.

    Args:
        league (): The `league` input parameter is used to modify the rules of a
            league.
        d (dict): The `d` input parameter is a dictionary that contains the new
            league rules as keys and values.

    """
    rules = d["values"]
    league.rules.min_games_total = rules["min_games_total"]
    league.rules.max_games_total = rules["max_games_total"]
    league.rules.players_per_match = rules["players_per_match"]
    league.rules.max_games_week = rules["max_games_week"]
    league.rules.min_games_day = rules["min_games_day"]
    league.rules.max_games_day = rules["max_games_day"]
    league.rules.max_week_gap = rules["max_week_gap"]
    league.rules.max_double_headers = rules["max_double_headers"]
    league.rules.min_captained = rules["min_captained"]
    league.rules.max_captained = rules["max_captained"]
    league.rules.minimum_subs_per_game = rules["minimum_subs_per_game"]
    league.rules.assume_busy = rules["assume_busy"] == "assume_busy"


def remove_player(league, d):
    """
    The function "remove_player" removes a player from the club's roster based on
    their ID.

    Args:
        league (dict): The `league` input parameter is used to specify the league
            object where the player should be removed.
        d (dict): The `d` parameter is a dictionary containing an ID for the player
            to be removed.

    """
    player = league.club.get_player_by_id(d["ids"]["player"])
    league.remove_player(player)


def change_flight(league, d):
    """
    This function changes the flight of a player from their current flight to the
    new flight specified by "d['values']['new_flight']".

    Args:
        league (dict): The `league` input parameter is used to pass the league
            object that the function should operate on.
        d (dict): The `d` input parameter is a dictionary that contains the new
            flight information and the player ID to be added to the new flight.

    """
    player = league.club.get_player_by_id(d["ids"]["player"])
    flight = league.get_flight_by_id(d["values"]["new_flight"])
    for f in league.flights:
        league.remove_player_from_flight(player, f)
    flight.add_player(player)


def update_availability(league, d):
    # {'event': 'availability', 'ids': {'timeslot': 1, 'player': 10}, 'values': 2}
    """
    The function `update_availability` takes a league object and a dictionary `d`
    with id values for a timeslot and a player.

    Args:
        league (): The `league` input parameter is used to retrieve information
            from the league database.
        d (dict): The `d` input parameter contains the data being updated for
            availability tracking purposes.

    """
    ts = league.get_timeslot_by_id(d["ids"]["timeslot"])
    player = league.club.get_player_by_id(d["ids"]["player"])
    a = d["values"]
    availability = league.get_player_availability_object(player, ts)
    availability.availability = a


def push_time_slot(league, d):
    # {'event': 'push_time_slot', 'ids': -1, 'values': '2023-11-08 20:15:00'}
    """
    This function creates a time slot for a game or event taking into account the
    duration of the game and other schedule events that have been played by setting
    specific time limits that last between starts and end times which accommodate
    the scheduling duration for all previous league events as taken from get_game_duration().

    Args:
        league (dict): The `league` input parameter is used to specify the league
            object that the timeslot will be created for. It allows the function
            to access the league's properties and methods (e.g.
        d (dict): The `d` input parameter is an event dict containing the time
            slot information {'event': 'push_time_slot', 'ids': -1,'values':
            '2023-11-08 20:15:00'}

    """
    start_time = datetime.strptime(d["values"], "%Y-%m-%d %H:%M:%S")
    game_duration = league.get_game_duration()
    end_time = start_time + timedelta(minutes=game_duration)
    league.create_timeslot(start_time, end_time)


def apply_edits(league, updates):
    # priority
    """
    This function "apply_edits" takes a league and a list of updates as input and
    applies the appropriate changes to the league based on the type of update.

    Args:
        league (dict): The `league` input parameter is the object that contains
            all the information about the esports league and its teams/players/games.
        updates (dict): The `updates` input parameter is a list of dictionary
            objects representing various updates to the league's information.

    """
    for d in updates:
        match d["event"]:
            case "add_player_to_league":
                add_player_to_league(league, d)
            case "push_time_slot":
                push_time_slot(league, d)
    # others
    for d in updates:
        print(d)
        match d["event"]:
            case "facility_in_league":
                facility_to_league(league, d)
            case "name":
                league.name = d["values"]
            case "duration":
                update_game_duration(league, d)
            case "timeslot":
                update_timeslot(league, d)
            case "flight_name":
                update_flight_name(league, d)
            case "rule_update":
                update_league_rules(league, d)
            case "remove_player_from_league":
                remove_player(league, d)
            case "change_flight":
                change_flight(league, d)
            case "availability":
                update_availability(league, d)


def create_games_from_request(league, data):
    """
    This function creates a new game event for each game included within a PandaX
    data flight.

    Args:
        league (): The `league` input parameter is used to access other functions
            or methods of the same league object.
        data (dict): The `data` input parameter is a dictionary that contains the
            flight and game information. It is iterated over twice within the
            function: first for the outer loop over all flights within the given
            league data and then for each game within a specific flight.

    """
    league.delete_all_game_events()
    for flight in data:
        for game in flight["games"]:
            flight = league.get_flight_by_id(game["flight"])
            timeslot = league.get_timeslot_by_id(game["timeslot"])
            facility = league.club.get_facility_by_id(game["facility"])
            if game["captain"] != -1:
                captain = league.club.get_player_by_id(game["captain"])
            else:
                captain = league.club.get_player_by_id(game["players"][0])
            players = []
            for p in game["players"]:
                players.append(league.club.get_player_by_id(p))
            league.create_game_event(
                players, facility, timeslot, flight, captain=captain
            )

def create_game_from_scheduler(league, flight, game):
    """
    This function creates a new game event for a given league using the information
    provided.

    Args:
        league (int): The `league` input parameter provides access to the league
            object which contains information such as clubs and their facilities.
        flight (int): The `flight` input parameter specifies the flight number of
            the game event.
        game (dict): The `game` input parameter is a dictionary containing information
            about the game to be created.

    """
    print('create ', game)
    timeslot = league.get_timeslot_by_id(game["timeslot"])
    facility = league.club.get_facility_by_id(game["facility"])
    if game["captain"] is not None:
        captain = league.club.get_player_by_id(game["captain"])
    else:
        captain = league.club.get_player_by_id(game["players"][0])
    players = []
    for p in game["players"]:
        players.append(league.club.get_player_by_id(p))
    league.create_game_event(
        players, facility, timeslot, flight, captain=captain
    )


def create_player_objects(flight, league, rules):
    """
    This function creates a list of `Player` objects from a flight's player
    associations and computes the mean availability score for the players based
    on league availability data.

    Args:
        flight (): The `flight` input parameter is a list of player associations
            from which the function creates players.
        league (dict): The `league` input parameter is used to retrieve player
            availability information for each player association.
        rules (dict): The `rules` input parameter defines the ruleset for player
            creation; it is used to initialise the player object's attributes like
            avg.

    Returns:
        list: The output returned by the `create_player_objects` function is a
        list of `Player` objects. Each `Player` object has an `id`, `rules`, and
        an `availability_score` attribute set based on the player's availability
        according to the `league` object's `get_player_availability_dict`. The
        `mean_availability_score` variable is computed as the average availability
        score of all players and each player's `availability_score` attribute is
        set relative to this mean.

    """
    players = []
    mean_availability_score = 0
    for a in flight.player_associations:
        avail = league.get_player_availability_dict(a.player)
        p = Player(a.player.id, rules, avail)
        mean_availability_score += p.availability_score
        players.append(p)
    mean_availability_score /= len(players)
    for p in players:
        p.set_availability_score_relation(mean_availability_score)
    return players

def create_gameslot_objects(league, rules):
    """
    This function creates a list of `GameSlot` objects based on the availability
    of facilities and timeslots for a given league.

    Args:
        league (): The `league` input parameter is a League object that provides
            information about the available timeslots and facility associations
            for scheduling games.
        rules (): The `rules` input parameter defines the game slot object's
            parameters and restrictions such as scoring format or duration constraints.

    Returns:
        list: The output returned by this function is a list of `GameSlot` objects.

    """
    gameslots = []
    for t in league.timeslots:
        for f in league.facility_associations:
            if f.facility.is_available(t):
                y2k_counter = t.since_y2k
                gs = GameSlot(t.id, f.id, y2k_counter, rules)
                gameslots.append(gs)
    return gameslots


def schedule_wizard(league, flight_id):
    """
    This function creates a scheduling system for a single flight of games using
    a league's rules and player information.

    Args:
        league (): The `league` input parameter passes the league object to the function.
        flight_id (int): The `flight_id` input parameter specifies the unique
            identifier of the flight for which to schedule games.

    """
    print("Schedule", league, flight_id)
    rules = league.get_league_rules_dict()
    flight = league.get_flight_by_id(flight_id)
    flight.delete_all_game_events()
    players = create_player_objects(flight, league, rules)
    gameslots = create_gameslot_objects(league, rules)
    generateGameSlotAvailabilityScores(gameslots, players)
    print('Create Scheduler')
    scheduler = SingleFlightScheduleTool(flight.id, rules, players, gameslots)
    print('Run Scheduler')
    scheduler.runCA()
    print('Assign Captains')
    scheduler.assign_captains()
    print('Build New Schedule')
    events = scheduler.return_events()
    # print('GAMES:', events)
    for e in events:
        create_game_from_scheduler(league, flight, e)
