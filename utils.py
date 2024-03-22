import os


def get_env_variable(variable):
    '''Get the value of an environment variable or throw exception.'''
    var_value = os.getenv(variable)
    
    if var_value is None:
        raise Exception(f"Environment variables {variable} is missing.")
    else:
        return var_value