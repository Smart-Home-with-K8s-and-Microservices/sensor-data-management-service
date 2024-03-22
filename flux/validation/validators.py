import re

from flux.validation import constants
from flux.validation.utils import (boundary_in_secs, is_datetime_boundary,
                                   is_duration_boundary)


def is_valid_boundary(boundary_input):
    '''Check if the input is a valid boundary for the start and stop parameters of the 'range()' flux funtion.'''
    return any([is_datetime_boundary(boundary_input),
                is_duration_boundary(boundary_input),])


def is_valid_range(start_value, stop_value):
    '''
    Validate if the provided start and stop values create a valid range for the 'range()' flux funtion.
    The stop value should not represent a more recent duration than the start value.

    Example:
    - Valid: start='-5m', stop='-2m' (a 3-minute range).
    - Invalid: start='-5m', stop='-5mo' (stop is more recent than start).
    '''
    start_bound_in_secs = boundary_in_secs(start_value)
    stop_bound_in_secs = boundary_in_secs(stop_value)

    if not all([start_bound_in_secs, stop_bound_in_secs]):
        return False

    return stop_bound_in_secs < start_bound_in_secs


def is_valid_method(method, numeric_records_only=False):
    '''Check if the provided method is a valid flux aggregation method.
       Supports additional aggregation methods when querying numeric records exclusively.'''

    valid_options = (
        constants.ALL_METHODS
        if numeric_records_only
        else constants.BASIC_METHODS
    )
    return method in valid_options


def is_method_with_window_support(method, numeric_records_only=False):
    '''Check if the provided method supports the time window option in the flux query.
       Supports additional aggregation methods when querying numeric records exclusively.'''
    valid_options = (
        constants.ALL_METHODS_WITH_WINDOW_SUPPORT
        if numeric_records_only
        else constants.BASIC_METHODS_WITH_WINDOW_SUPPORT
    )
    return method in valid_options


def is_valid_window(window_input):
    '''Check if the input is a valid time window of the 'window()' flux function.'''
    is_valid_window = re.match(constants.TIME_WINDOW_PATTERN, window_input)
    return is_valid_window
