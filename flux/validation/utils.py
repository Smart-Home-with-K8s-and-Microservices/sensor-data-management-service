import re
from datetime import datetime

from flux.validation.constants import (FLUX_UNITS, ISO_8601_FORMAT,
                                       RANGE_BOUND_PATTERN)


def boundary_in_secs(bound_input):
    '''Convert a provided input (flux duration format or ISO 8601 datetime) into seconds.
       In case of an invalid input, 'None' is returned'''

    # Regex expression for recognizing and dividing duration inputs
    # e.g. '5s' to 5 and 's' (seconds)
    # e.g. '12mo' to 12 and 'mo' (months)
    match = re.search(r"(\d+)([a-z]+)", bound_input)

    if match:
        # input is a valid flux duration
        bound_numeric_value = int(match.group(1))
        bound_time_unit = match.group(2)
        # convert to seconds based on the numeric value and the time unit
        return bound_numeric_value * FLUX_UNITS[bound_time_unit]
    else:
        try:
            # consider the input as an ISO 8601 datetime
            # subtract the input from the current datetime to convert to secs
            bound_as_datetime = datetime.strptime(bound_input, ISO_8601_FORMAT)
            current_datetime = datetime.now()
            time_difference = current_datetime - bound_as_datetime
            return time_difference.total_seconds()
        except ValueError:
            # not a valid flux duration format or an ISO 8601 datetime
            return None


def is_datetime_boundary(bound_input):
    '''Check if the boundary input is a valid ISO 8601 datetime.'''
    try:
        datetime.strptime(bound_input, ISO_8601_FORMAT)
        return True
    except ValueError:
        return False


def is_duration_boundary(bound_input):
    '''Check if the boundary input matches the flux duration pattern for range values.
       For example, '-5m' is a valid duration that corresponds to 5 minutes.'''
    return re.match(RANGE_BOUND_PATTERN, bound_input)
