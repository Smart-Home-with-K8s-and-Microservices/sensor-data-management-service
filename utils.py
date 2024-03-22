import os

REQUIRED_QUERY_PARAMS = ['start', 'stop']
OPTIONAL_QUERY_PARAMS = ['window', 'method', 'numeric_records_only']


def get_missing_params(request):
    '''Get missing required query parameters from the request.'''
    return REQUIRED_QUERY_PARAMS - request.args.keys()


def get_params_per_category(request):
    '''Get query parameters categorized into basic (required and optional) 
    and filtering parameters (the rest).'''
    basic_params = {}
    filtering_params = {}

    for key, value in request.args.items():
        if key in REQUIRED_QUERY_PARAMS + OPTIONAL_QUERY_PARAMS:
            basic_params[key] = value
        else:
            filtering_params[key] = value
    return basic_params, filtering_params


def get_env_variable(variable):
    '''Get the value of an environment variable or throw exception.'''
    var_value = os.getenv(variable)
    
    if var_value is None:
        raise Exception(f"Environment variables {variable} is missing.")
    else:
        return var_value