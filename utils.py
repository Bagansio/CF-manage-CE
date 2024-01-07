import os
import json
from exceptions import *

INSTANCE_CHANGING_STATUS = ['PROVISIONING','STAGING','STOPPING','REPAIRING','SUSPENDING']

"""
Returns the needed environment variables

if them not exists throws a ValueError Exception
"""
def get_env_variables():
    
    env = dict(
        project = os.environ.get("instance_project", None),
        zone = os.environ.get("instance_zone", None),
        name = os.environ.get("instance_name", None)
    )

    if None in env.values():
        raise ServerException("ERROR: One or more required environment variables are missing.")

    return env

def generate_response(message, status=200):
    response = {'status': status, 'message': message}
    return json.dumps(response),  status

def generate_error_response(message, status):
    response = {'status': status, 'error': message}
    return json.dumps(response), status


def handle_on(instances_client, instance_data, env):

    if instance_data.status == "RUNNING":
        raise BadRequestException(f"ERROR: Instance is already on")
    
    start_status = instances_client.start(project=env['project'], zone=env['zone'], instance=env['name'])
    
    return generate_response("INSTANCE ON")

def handle_off(instances_client, instance_data, env):

    if instance_data.status == "TERMINATED":
        raise BadRequestException(f"ERROR: Instance is already off")
    
    stop_status = instances_client.stop(project=env['project'], zone=env['zone'], instance=env['name'])
    
    return generate_response("INSTANCE OFF")