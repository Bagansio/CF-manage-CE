---
title: Cloud Function for Turning On or Off a Compute Engine Instance
subtitle: A Cloud Function that turns on or off a Compute Engine instance using an HTTP request
---

This Cloud Function allows you to turn on or off a Compute Engine instance using an HTTP request.

### Deployment
To deploy the function, use the following command:

```bash
gcloud functions deploy <cf_name> \
--gen2 \
--region=<region> \
--runtime=python312 \
--entry-point=instance_on_off \
--trigger-http \
--<CF-ServiceAccount> \
--set-env-vars instance_project="<instance_project>",instance_name="<instance_name>",instance_zone="<instance_zone>"
```

Replace `<cf_name>` with your desired CF name, `<region>` with your project's region, `<CF-ServiceAccount>` with the service account ID of the service account that will be used to access the Cloud Functions runtime, and `<instance_project>`, `<instance_name>`, and `<instance_zone>` with the project ID, instance name, and zone of the Compute Engine instance that you want to control.

Before deploying your function, make sure that your service account has the following roles:

* Cloud Functions Service Agent: This role is required for the function to execute.
* Compute Instance Admin (beta): This role is required for the function to start and stop Compute Engine instances.
* Service Account Use: This role is required for the function to impersonate other service accounts when accessing resources.



### Usage
To turn on the instance, send a POST request to the function's URL with the following JSON body:

```json
{
  "instance": "on" //off
}
```

#### Example of usage

curl -m 70 -X POST <CF_URL> -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{
  "instance": "off"
}'