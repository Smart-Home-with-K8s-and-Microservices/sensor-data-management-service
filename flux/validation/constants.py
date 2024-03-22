ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
RANGE_BOUND_PATTERN = r'^-\d+(ns|us|ms|s|m|h|d|w|mo|y)$'
TIME_WINDOW_PATTERN = r'^\d+(ns|us|ms|s|m|h|d|w|mo|y)$'

FLUX_UNITS = {
    'ns': 1e-9,  # nanoseconds to seconds
    'us': 1e-6,  # microseconds to seconds
    'ms': 1e-3,  # milliseconds to seconds
    's': 1,  # seconds
    'm': 60,  # minutes to seconds
    'h': 3600,  # hours to seconds
    'd': 86400,  # days to seconds
    'w': 604800,  # weeks to seconds
    'mo': 2628000,  # months to seconds (approximate)
    'y': 31536000,  # years to seconds (approximate)
}

ALL_METHODS = [
    'mean',
    'median',
    'max',
    'min',
    'sum',
    'derivative',
    'distinct',
    'count',
    'increase',
    'skew',
    'spread',
    'stddev',
    'first',
    'last',
    'unique',
    'sort',
]

ALL_METHODS_WITH_WINDOW_SUPPORT = [
    'max',
    'min',
    'derivative',
    'increase',
    'first',
    'last',
    'unique',
    'sort',
]

# List of basic aggregation methods
# that support querying time series records of any value type,
# including booleans and strings
BASIC_METHODS = [
    'count',
    'distinct',
    'first',
    'last',
    'unique',
    'sort'
]

BASIC_METHODS_WITH_WINDOW_SUPPORT = list(
    set(BASIC_METHODS) & set(ALL_METHODS_WITH_WINDOW_SUPPORT)
)
