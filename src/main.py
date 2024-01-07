from google.cloud import compute_v1
from utils import *
from exceptions import *

"""
Function that modifies status of a compute engine instance specified by environment variables (instance_project, instance_zone, instance_name)

if GET:
    returns compute engine instance status

if POST:
    turns on/off a compute engine instance

"""
def instance_on_off(request):
    try:
        env = get_env_variables() 
        
        instances_client = compute_v1.InstancesClient()

        instance_data = instances_client.get(project=env['project'], zone=env['zone'], instance=env['name'])

        if request.method == "GET":
            return generate_response(f"Instance status is {instance_data.status}") 
        
        if request.method != "POST":
            raise BadRequestException("Only methods allowed are GET/POST")
        
        data = request.json

        if not 'instance' in data or data['instance'] not in ["on", "off"]:
            raise BadRequestException("ERROR: request only accepts 'instance': 'on'/'off'")

        if instance_data.status in INSTANCE_CHANGING_STATUS:
            raise ToManyException(f"ERROR: Instance is currently {instance_data.status}. Try again later")

        if data['instance'] == "on":
            return handle_on(instances_client, instance_data, env)
        
        return handle_off(instances_client, instance_data, env)
    
    except GeneralException as exception:
        return generate_error_response(exception.error_code, exception.message)