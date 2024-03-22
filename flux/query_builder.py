from .validation.exceptions import (InvalidBoundaryException,
                                    InvalidMethodException,
                                    InvalidMethodWithWindowException,
                                    InvalidRangeException,
                                    InvalidTimeWindowException)
from .validation.validators import (is_method_with_window_support,
                                    is_valid_boundary, is_valid_method,
                                    is_valid_range, is_valid_window)


class FluxQueryBuilder:
    def __init__(self, bucket, start, stop, method=None, window=None,
                 numeric_records_only=False):
        '''
        Initialize a FluxQueryBuilder.

        A validation process checks if the provided data can create a valid Flux query.

        By default, it assumes the queried records may contain non-numeric data.
        Set numeric_records_only to True if your records are exclusively numeric.
        '''
        self.validate_params(start, stop, method, window, numeric_records_only)

        self.bucket = bucket
        self.start = start
        self.stop = stop
        self.filters = {}
        self.method = method
        self.window = window
        self.numeric_records_only = numeric_records_only

    @classmethod
    def validate_params(cls, start, stop, method, window,
                        numeric_records_only=False):
        '''Check if the provided query parameters can create a valid flux query'''
        if not is_valid_boundary(start):
            raise InvalidBoundaryException(start)
        if not is_valid_boundary(stop):
            raise InvalidBoundaryException(stop)
        if not is_valid_range(start, stop):
            raise InvalidRangeException
        if method and not is_valid_method(
                method, numeric_records_only):
            raise InvalidMethodException(method, numeric_records_only)
        if window and not is_valid_window(window):
            raise InvalidTimeWindowException(window)
        if (all([method, window, not is_method_with_window_support(
                method, numeric_records_only)])):
            raise InvalidMethodWithWindowException(
                method, numeric_records_only)
        return True

    def validate_assigned_params(self):
        '''Check if the assigned to the instance parameters can create a valid flux query'''
        self.validate_params(self.start, self.stop,
                             self.method, self.window, self.numeric_records_only)

    def set_bucket(self, bucket):
        self.bucket = bucket

    def set_start(self, start):
        self.start = start

    def set_stop(self, stop):
        self.stop = stop

    def set_method(self, method):
        self.method = method

    def set_window(self, window):
        self.window = window

    def add_filter(self, filter_key, filter_value):
        key_str = str(filter_key)
        value_str = str(filter_value)
        self.filters[key_str] = value_str

    def delete_filters(self):
        self.filters = {}

    def build_query_string(self):
        '''Generate a Flux query string based on the instance's query parameters.
           If you manually modify the instance parameters,
           remember to run validate_assigned_params() for revalidation
           before generatring the query.'''
        query_parts = [
            f'from(bucket: "{self.bucket}")',
            f'|> range(start: {self.start}, stop: {self.stop})',
            *[f'|> filter(fn: (r) => r["{filter_key}"] == "{filter_value}")'
                for filter_key, filter_value in self.filters.items()],
        ]
        if self.window:
            query_parts.append(f'|> window(every: {self.window})')
        if self.method:
            query_parts.append(f'|> {self.method}()')

        return ''.join(query_parts)
