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
    player.rules["minGamesTotal"] = 0

def maxDoubleHeadersDay_exception(player):
    player.rules["maxGamesDay"] = 2
    player.rules["maxGamesWeek"] = 2

def maxDoubleHeadersWeek_exception(player):
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
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def log_timer(func):
    def wrapper(*args, **kwargs):
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
    gs = []
    for g in gameslots:
        gs.append(g.duplicate())
    return gs