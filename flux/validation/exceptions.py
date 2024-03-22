from flux.validation.constants import (ALL_METHODS,
                                       ALL_METHODS_WITH_WINDOW_SUPPORT,
                                       BASIC_METHODS,
                                       BASIC_METHODS_WITH_WINDOW_SUPPORT,
                                       FLUX_UNITS)

'''Module for custom exceptions with descriptive error messages for invalid Flux Query parameters.'''


class InvalidQueryException(Exception):
    '''Generic parent class exception related to validation errors when building a Flux Query'''


class InvalidBoundaryException(InvalidQueryException):
    def __init__(self, bound_input):
        self.instructions = (
            'The pattern should be an ISO 8601 datetime (YY-MM-DDThh:mm:ssZ) or '
            'in the format: -<number><unit>, where unit is one of '
            f'{list(FLUX_UNITS.keys())}.')
        super().__init__(
            f'Invalid format \'{bound_input}\' for boundary value. {self.instructions}'
        )


class InvalidRangeException(InvalidQueryException):
    def __init__(self):
        super().__init__('Conflict in range boundaries or invalid format.')


class InvalidMethodException(InvalidQueryException):
    def __init__(self, method, numeric_records_only=False):
        self.valid_options = (
            ALL_METHODS if numeric_records_only else BASIC_METHODS)
        super().__init__(
            f'Invalid method \'{method}\'. Valid options are: {", ".join(self.valid_options)}'
        )


class InvalidMethodWithWindowException(InvalidQueryException):
    def __init__(self, method_input, numeric_records_only=False):
        self.valid_options = (
            ALL_METHODS_WITH_WINDOW_SUPPORT
            if numeric_records_only
            else BASIC_METHODS_WITH_WINDOW_SUPPORT
        )
        super().__init__(
            f'Method \'{method_input}\' does not support a time window. Valid methods with window support: {self.valid_options}.'
        )


class InvalidTimeWindowException(InvalidQueryException):
    def __init__(self, window_input):
        self.instructions = f'The pattern should be: <number><unit>, where unit is one of {list(FLUX_UNITS.keys())}'
        super().__init__(
            f'Invalid format \'{window_input}\' for time window value. {self.instructions}'
        )
