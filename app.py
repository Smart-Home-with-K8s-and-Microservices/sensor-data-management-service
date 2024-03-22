import utils
from db.service import InfluxDBService
from flask import Flask, jsonify, request
from flux.query_builder import FluxQueryBuilder
from flux.validation.exceptions import InvalidQueryException
from influxdb_client.rest import ApiException as InfluxClientAPIException

# Get InfluxDB credentials from envs or throw exception
bucket = utils.get_env_variable('DOCKER_INFLUXDB_INIT_BUCKET')
token = utils.get_env_variable('DOCKER_INFLUXDB_INIT_ADMIN_TOKEN')
org = utils.get_env_variable('DOCKER_INFLUXDB_INIT_ORG')
protocol = utils.get_env_variable('DOCKER_INFLUXDB_HOST_TYPE')
host = utils.get_env_variable('DOCKER_INFLUXDB_HOST')
port = utils.get_env_variable('DOCKER_INFLUXDB_PORT')
url = f'{protocol}://{host}:{port}'

app = Flask(__name__)

@app.route('/records', methods=['GET'])
def list_records():
    '''
    A generic endpoint for querying InfluxDB.
    By utilizing URL query parameters, you can specify the following options:
     - bucket* => The name of the bucket containing your desired time series data
     - start* => Earliest time to include in results (e.g. '-5m' or '2023-11-01T12:00:00Z')
     - stop* => Latest time to include in results (e.g. '-2m' or '2023-12-01T12:00:00Z') )
     - method => The name of a desired aggregation method to execute on the time series data (e.g. 'count')
     - window => Time window to group the results on time bounds (e.g. '1m')
     - numeric_records_only [default=False] => Numeric records support more aggregation methods.
       Set this if you know you are quering numeric records exclusively and you want to enable a wider range of aggregation methods.
     - <every-other-keyword> => Every other key-value query parameter is applied as a filter (e.g. device_type=robot) to the query.

    *required
    '''
    missing_params = utils.get_missing_params(request)

    if missing_params:
        return jsonify(errors=f'Missing required query parameters: [{", ".join(missing_params)}]'), 400

    # try to establish a connection with InfluxDB
    influxdb_instance = InfluxDBService(url, token, org)
    
    if not influxdb_instance.is_active():
        influxdb_instance.close_connection()
        return jsonify(error='Error while connecting to InfluxDB.'), 500

    try:
        basic_params, filtering_params = utils.get_params_per_category(request)

        # attempt to create a flux query instance 
        # by also validating the given parameters
        flux_query_instance = FluxQueryBuilder(bucket, **basic_params)

        # include all additional query parameters, 
        # not among the basic ones, as filters in the Flux query.
        for param_key, param_value in filtering_params.items():
            flux_query_instance.add_filter(param_key, param_value)

        # generate the flux query string and run it
        flux_query = flux_query_instance.build_query_string()
        results = influxdb_instance.run_query(flux_query)

        response = jsonify(data=results)
    
    except InvalidQueryException as e:
        # Handle exceptions related to building 
        # an invalid query with the Flux Query Builder
        response = jsonify(error=str(e)), 400
    
    except InfluxClientAPIException as e:
        # Handle exceptions generated when executing 
        # the Flux query on the InfluxDB service
        response = jsonify(error=e.message), e.status
    
    except Exception as e:
        # Handle any other unexpected exceptions
        response = jsonify(error=str(e)), 500
    
    finally:
        influxdb_instance.close_connection()

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
