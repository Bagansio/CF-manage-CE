from google.cloud import compute_v1
import os

INSTANCE_CHANGING_STATUS = ['PROVISIONING','STAGING','STOPPING','REPAIRING','SUSPENDING']

def instance_on_off(request):

    env = get_env_variables()

    if None in env.values():
        return ("ERROR FROM CLOUD FUNCTION",500) 
    
    instances_client = compute_v1.InstancesClient()

    instance_data = instances_client.get(project=env['project'], zone=env['zone'], instance=env['name'])

    if request.method == "GET":
        return f"Instance status is {instance_data.status}" 
    
    data = request.json

    if not 'instance' in data or data['instance'] not in ["on", "off"]:
        return ("ERROR: request only accepts 'instance': 'on'/'off'", 400)

   

    if instance_data.status in INSTANCE_CHANGING_STATUS:
        return (f"ERROR: Instance is currently {instance_data.status}. Try again later", 429)

    if data['instance'] == "on":
        return handle_on(instances_client, instance_data, env)
    
    return handle_off(instances_client, instance_data, env)
    

def get_env_variables():
    env = dict(
            project = os.environ.get("instance_project", None),
            zone = os.environ.get("instance_zone", None),
            name = os.environ.get("instance_name", None),
        )
    
    return env

def handle_on(instances_client, instance_data, env):

    if instance_data.status == "RUNNING":
        return (f"ERROR: Instance is already on",400)
    
    start_status = instances_client.start(project=env['project'], zone=env['zone'], instance=env['name'])
    
    return "INSTANCE ON"

def handle_off(instances_client, instance_data, env):

    if instance_data.status == "TERMINATED":
        return (f"ERROR: Instance is already off", 400)
    
    stop_status = instances_client.stop(project=env['project'], zone=env['zone'], instance=env['name'])
    
    return "INSTANCE OFF"