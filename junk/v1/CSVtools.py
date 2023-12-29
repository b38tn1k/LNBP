from app import db
from app.forms import CSVUploadForm
from app.models.player import Player
from app.models.club import Club
import csv
import os
from dateutil.parser import parse
from datetime import timedelta
from werkzeug.utils import secure_filename
import json


UPLOAD_FOLDER = 'app/uploads/'


def read_csv(filename):
    # Read the CSV content
    """
    The function `read_csv(filename)` reads the contents of a CSV file specified
    by `filename` and returns a list of rows (cells) as a single-dimensional list.

    Args:
        filename (str): The `filename` input parameter is the name of the file to
            be read.

    Returns:
        list: The output returned by this function is a list of lists named "csv_content".

    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        csv_content = list(reader)
    return csv_content


def get_schedule_blocks(csv_content):
    # Indices where rows are fully empty
    """
    This function finds blocks of consecutive empty rows (rows with no cells)
    within a CSV content and returns a list of tuples representing the start and
    end indices of each block.

    Args:
        csv_content (list): The `csv_content` parameter is the 2D list of rows and
            columns representing the CSV data to be processed by the function.

    Returns:
        list: The output returned by this function is a list of pairs of indices
        (starting index and ending index) for each block of non-empty rows found
        within the given CSV content.

    """
    empty_row_indices = [i for i, row in enumerate(csv_content) if not any(row)]
    # Add start and end indices for csv_content
    empty_row_indices.insert(0, -1)
    empty_row_indices.append(len(csv_content))
    # Create pairs of indices for each block
    block_indices = [(start + 1, end) for start, end in zip(empty_row_indices[:-1], empty_row_indices[1:]) if end - start > 1]

    return block_indices


def process_schedule_block(csv_content, start, end):
    # Extract headers
    """
    This function processes a CSV file containing information about basketball
    players and their availability for games on specific days and times. It extracts
    headers from the first few rows of the file (date and time headers), parses
    the date and time strings into actual dates and times using the `datetime`
    module's `parse()` method. The function then iterates over the remaining rows
    of the CSV file and creates a list of players with their availability for each
    game and their names.

    Args:
        csv_content (str): The `csv_content` input parameter is a list of
            comma-separated values representing a schedule block data set and is
            used to extract the flight name date and time information and process
            each player's availability for a specific date and time range.
        start (int): The `start` input parameter specifies the index of the first
            row to process within the CSV content.
        end (int): The `end` input parameter specifies the index of the last row
            to be processedin the CSV file. It is used to skip the header row and
            any additional rows that may exist at the end of the file.

    """
    if (start + 1 >= len(csv_content)):
        return
    date_headers = csv_content[start]
    time_headers = csv_content[start + 1]

    flight_name = date_headers[0]

    timeslots = []
    last_date = ""

    for date, time in zip(date_headers, time_headers):
        if date:  # Check if there's a date value
            last_date = date.strip()
        if time:  # Append to timeslots only if there's a time value
            try:
                datetime_obj = parse(f"{last_date} {time.strip()}")
                timeslots.append(datetime_obj)
            except:
                # (flight_name, " no date")
                pass
    players = []
    potential_courts = {}
    # Process each player row
    for i in range(start + 2, end):
        row = csv_content[i]
        name = row[0]
        availability = []
        games = []
        low_availability_games = []
        
        for cell in row[1:]:
            if '-' in cell:
                availability.append(2)
            elif 'X' in cell.upper():
                availability.append(3)
            else:
                availability.append(1)
                if cell in potential_courts:
                    potential_courts[cell] += 1
                else:
                    if cell:
                        potential_courts[cell] = 1
            if cell in potential_courts:
                games.append(cell)
            else:
                games.append("")

        player = {
            'name': name,
            'availability': availability,
            'games': games
        }

        players.append(player)
    keys_to_delete = []
    for key, value in potential_courts.items():
        if key.startswith('C') and key[1:] in potential_courts:
            potential_courts[key[1:]] += value
            keys_to_delete.append(key)
        elif potential_courts[key] < 2:
            keys_to_delete.append(key)
        else:
            pass
    captain_court_range = set()
    court_range = set()
    for key in keys_to_delete:
        del potential_courts[key]
    for key in potential_courts:
        court_range.add(key)
        captain_court_range.add('C' + key)
    for p in players:
        for i, g in enumerate(p['games']):
            if not (g in court_range or g in captain_court_range):
                p['games'][i] = ''
    # HACK
    court_range = {1, 2, 3, 4, 5}
    #HACK
    return flight_name, court_range, timeslots, players


def get_number_of_columns(csv_file_path):
    """
    This function gets the number of columns present inside a given CSV file by
    reading the first row and then returning the length of that row.

    Args:
        csv_file_path (str): The `csv_file_path` input parameter specifies the
            file path to the CSV file that should be read by the function.

    Returns:
        int: The output returned by this function is the number of columns present
        inthe first row of the CSV file specified by the `csv_file_path` argument.

    """
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        first_row = next(csv_reader)
        return len(first_row)
    

def get_court_name(name, courts):
    """
    This function takes a string `name` and an list of dictionaries `courts`, where
    each dictionary represents a court with a `court_name`.

    Args:
        name (str): The `name` input parameter is a string that represents the
            full name of the court to be searched.
        courts (list): The `courts` input parameter is a list of courts and the
            function iterates over it to find the court with the matching name.

    Returns:
        str: The output returned by this function is `name`, which is the original
        input string minus the first character (a space).

    """
    for c in courts:
        if c.court_name == name[1:]:
            name = name[1:]
            break
    return name
    

def unpack_long_csv(club, filepath):
    """
    This function unpacks a long CSV file containing data for a single flight of
    matches and creates the flights and players' availability records.

    Args:
        club (): The `club` input parameter is used to retrieve or add courts and
            players to the club based on the data from the CSV file.
        filepath (str): The `filepath` parameter is a string that contains the
            path to a CSV file containing the scheduling data.

    """
    csv_content = read_csv(filepath)
    league_name = filepath.split('.')[0].split('/')[-1]
    league = club.add_league(league_name)
    for start, end in get_schedule_blocks(csv_content):
        flight_name, court_range, timeslots, players = process_schedule_block(csv_content, start, end)
        # 1. make sure all the courts exist and collect them for the flight
        courts = []
        for c in court_range:
            result = club.get_court_by_name(c)
            if result:
                courts.append(result)
            else:
                court = club.add_court(c)
                courts.append(court)
        # 2. create the flight with the courts
        flight = league.add_flight(flight_name)
        print(flight.id)
        tsids = []
        for t in timeslots:
            r = flight.create_timeslot(t, t + timedelta(hours=1), courts)
            tsids.append(r)
        # 4. create or find the players
        games = {}
        for p in players:
            player_name = p['name']
            player_email = p['name']+'@email.com'
            r = club.add_player(player_name, player_email)
            flight.add_player(r)
            availability = []
            for i, a in enumerate(p['availability']):
                if (i < len(tsids)):
                    # 5. fill out the player availability
                    availability.append({'timeSlotId': tsids[i], 'availability': int(a)})
                    if not tsids[i] in games:
                        games[tsids[i]] = {}
                    if p['games'][i]:
                        g_court = get_court_name(p['games'][i], courts)
                        if not g_court in games[tsids[i]]:
                            games[tsids[i]][g_court] = {'captain': None, 'players': [] }
                        games[tsids[i]][g_court]['players'].append(r)
                        if 'C' in p['games'][i]:
                            games[tsids[i]][g_court]['captain'] = r

            # print(availability)
            availability_data = {}
            if r.availability_data:
                availability_data = json.loads(r.availability_data)
            # Update or add the availability for the specified flight
            availability_data[str(flight.id)] = availability
            # Save the updated availability data to the player's availability_data column
            r.availability_data = json.dumps(availability_data)
            
        db.session.commit()
        # 6. create any events if they dont
        for tsid in games:
            timeslot = flight.get_timeslot_by_id(tsid)
            if timeslot:
                for court in games[tsid]:
                    court_obj = club.get_court_by_name(court)
                    timeslot.create_event(court_obj, games[tsid][court]['players'], games[tsid][court]['captain'])

        db.session.commit()


def createFileForm(club):
    # test
    # club.empty()
    # db.session.commit()
    # test
    """
    This function creates a form for uploading CSV files to a Django app and
    performs the following operations on the uploaded file:
    1/ Validates the file upload and saves it to a specific folder based on the
    club ID.
    2/ Extracts the number of columns from the file and unpacks long CSV files
    (more than 4 columns).
    3/ Loads players from the CSV file into the club.

    Args:
        club (): The `club` input parameter is used to specify the Club object
            that the uploaded CSV file will be associated with. The function creates
            a file form for uploading CSV files and validates the form inputs.

    Returns:
        : The output returned by this function is a CSVUploadForm instance.

    """
    fileform = CSVUploadForm()
    if fileform.validate_on_submit():
        f = fileform.file.data
        filename = secure_filename(f.filename)
        club_folder = os.path.join(UPLOAD_FOLDER, str(club.id))
        if not os.path.exists(club_folder):
            os.makedirs(club_folder)
        filepath = os.path.join(club_folder, filename)
        f.save(filepath)
        type_by_length = get_number_of_columns(filepath)
        if type_by_length > 4:
            unpack_long_csv(club, filepath)
            # for p in club.players:
                # print(p)
                # print([f for f in p.flights])
        else:  #just load the players
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if (row[0] and row[1]):
                        club.add_player(row[0], row[1])
    return fileform