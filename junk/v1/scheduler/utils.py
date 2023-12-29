import time
import random
import string

AVAILABLE = 1
AVAILABLE_LP = 2
UNAVAILABLE = 3
UNK = -1

POOL_ITERATIONS = 1000 # is a modifier based on player count
ATTEMPTS = 20

tempRules = {}
tempRules["assumeBusy"] = False  # YES
tempRules["minGamesTotal"] = 4  # YES
tempRules["maxGamesTotal"] = 4  # YES
tempRules["minGamesDay"] = 0  # TODO
tempRules["maxGamesDay"] = 1  # YES - but also allow double header implementation
tempRules["minGamesWeek"] = 0  # TODO
tempRules["maxDoubleHeaders"] = 0  # TODO
tempRules["maxConcurrentGames"] = 2  # TODO
tempRules["maxGamesWeek"] = 1  # YES
tempRules["minCaptained"] = 1  # TODO
tempRules["maxCaptained"] = -1  # TODO
tempRules["maxWeekGap"] = 2  # TODO
tempRules["playersPerMatch"] = 4  # YES
tempRules["minimumSubsPerGame"] = 0.7  # YES

exceptions = {}
exceptions["assumeBusy"] = []
exceptions["minGamesTotal"] = [7, 116, 123, 124, 115]
exceptions["maxGamesTotal"] = []
exceptions["minGamesDay"] = []
exceptions["maxGamesDay"] = []
exceptions["minGamesWeek"] = []
exceptions["maxGamesWeek"] = []
exceptions["minCaptained"] = []
exceptions["maxCaptained"] = []
exceptions["maxWeekGap"] = []
exceptions["maxDoubleHeadersDay"] = []
exceptions["maxDoubleHeadersWeek"] = [7, 116, 123, 124, 115]
tempRules["except"] = exceptions

function_metrics = {}

def minGamesTotal_exception(player):
    """
    This function sets the "minGamesTotal" rule for the given player to 0.

    Args:
        player (dict): The `player` input parameter is used to access the `rules`
            dictionary of the player object and modify its value for the "minGamesTotal"
            key.

    """
    player.rules["minGamesTotal"] = 0

def maxDoubleHeadersDay_exception(player):
    """
    This function sets the "maxGamesDay" and "maxGamesWeek" rules for the provided
    player to 2.

    Args:
        player (dict): The `player` input parameter is not used anywhere inside
            the function `maxDoubleHeadersDay_exception`.

    """
    player.rules["maxGamesDay"] = 2
    player.rules["maxGamesWeek"] = 2

def maxDoubleHeadersWeek_exception(player):
    """
    This function sets the `maxGamesWeek` rule for the given `player` to 2.

    Args:
        player (dict): The `player` input parameter is not used anywhere inside
            the `maxDoubleHeadersWeek_exception` function.

    """
    player.rules["maxGamesWeek"] = 2

exception_fixers = {}
exception_fixers["assumeBusy"] = None
exception_fixers["minGamesTotal"] = minGamesTotal_exception
exception_fixers["maxGamesTotal"] = None
exception_fixers["minGamesDay"] = None
exception_fixers["maxGamesDay"] = None
exception_fixers["minGamesWeek"] = None
exception_fixers["maxGamesWeek"] = None
exception_fixers["minCaptained"] = None
exception_fixers["maxCaptained"] = None
exception_fixers["maxWeekGap"] = None
exception_fixers["maxDoubleHeadersDay"] = maxDoubleHeadersDay_exception
exception_fixers["maxDoubleHeadersWeek"] = maxDoubleHeadersWeek_exception

def update_availability_template(availability_template, availability, assume_busy):
    """
    This function takes an availability template and updates it with new availability
    information.

    Args:
        availability_template (dict): The `availability_template` input parameter
            is used as a copy of the initial availability template and is modified
            within the function to reflect the updated availability state based
            on the provided `availability` information.
        availability (dict): The `availability` input parameter is used to specify
            a list of dictionaries representing available time slots with their
            corresponding availability statuses.
        assume_busy (bool): The `assume_busy` input parameter tells the function
            to mark as unavailable any time slots that are not explicitly marked
            as available or unavailable.

    Returns:
        dict: The function returns two things:
        
        1/ A score (an integer) that represents the number of available time slots
        out of the total number of time slots.
        2/ An updated availability template (a dictionary), where the values for
        each time slot have been updated based on the provided availability and
        assuming busy or not.

    """
    availability_template = availability_template.copy()  # Make a copy
    if availability:
        for item in availability:
            key = int(item["timeSlotId"])  # convert to int for comparison
            if key in availability_template:
                availability_template[key] = item["availability"]
    score = 0
    for key in availability_template:
        if availability_template[key] == UNK:
            if assume_busy:
                availability_template[key] = UNAVAILABLE
            else:
                availability_template[key] = AVAILABLE
        if (
            availability_template[key] == AVAILABLE
            or availability_template[key] == AVAILABLE_LP
        ):
            score += 1

    return score, availability_template

def random_string(length):
    """
    The function `random_string` generates a string of a specified length using a
    combination of random ASCII letters and digits.

    Args:
        length (int): The `length` input parameter specifies the number of characters
            that the random string should have.

    Returns:
        str: The output returned by this function is a random string of length
        `length`, consisting of letters and digits chosen at random from the
        standard 7-bit ASCII character set.

    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def log_timer(func):
    """
    This function logs the execution time of a function and collects statistics
    on its performance.

    Args:
        func (): The `func` input parameter is a decorated function that is being
            wrapped by the `log_timer()` function.

    Returns:
        : The output returned by this function is the result of the wrapped function
        (`*args`, **kwargs) plus some timing information for that function call.

    """
    def wrapper(*args, **kwargs):
        """
        This function is a decorator that wraps another function `func` and measures
        its execution time.

        Returns:
            : The output returned by this function is the result of the function
            `func` with arguments `args` and `kwargs`, along with additional
            information about the execution time of the function.

        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time

        if func.__name__ not in function_metrics:
            function_metrics[func.__name__] = {
                "total_time": 0,
                "max_time": 0,
                "count": 0,
            }

        function_metrics[func.__name__]["total_time"] += elapsed_time
        function_metrics[func.__name__]["max_time"] = max(
            function_metrics[func.__name__]["max_time"], elapsed_time
        )
        function_metrics[func.__name__]["count"] += 1

        return result

    return wrapper


def timer_report():
    """
    This function sorts a list of metrics by the total time spent on each function
    and reports the average and maximum time for each function.

    """
    sorted_metrics = sorted(
        function_metrics.items(),
        key=lambda x: x[1]["total_time"],
        reverse=True,
    )
    for func_name, metrics in sorted_metrics:
        avg_time = metrics["total_time"] / metrics["count"]
        print(
            f"{func_name}: Total: {metrics['total_time']:.6f} Count: {int(metrics['count'])} Average: {avg_time:.6f} seconds, Max: {metrics['max_time']:.6f} seconds"
        )
        print()

def copy_gameslots(gameslots):
    """
    This function creates a copy of a list of game slots (gs) by duplicating each
    element of the input list (gameslots).

    Args:
        gameslots (list): The `gameslots` input parameter is a list of game slots
            that will be duplicated and returned as a new list by the function.

    Returns:
        list: The output of the function `copy_gameslots` is a list of duplicates
        of the original `gameslots` list.

    """
    gs = []
    for g in gameslots:
        gs.append(g.duplicate())
    return gs