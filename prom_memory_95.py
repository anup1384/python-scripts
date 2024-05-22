# from slack_sdk import WebClient
import requests, datetime
import json
import os

# Prometheus server URL
PROMETHEUS_URL = "http://192.168.0.1:9090/api/v1/query"
namespace = "prod"

date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Slack token and channel
# SLACK_TOKEN = 'your-slack-token'
# SLACK_CHANNEL = 'your-slack-channel'

# Slack webhook URL
#exampe = 'https://hooks.slack.com/services/T918992792/ABCFR1234/Anup1jjsjjuwuas'
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/T918992792/ABCFR1234/Anup1jjsjjuwuas'

# File to write pod names to
POD_FILE = 'memory_95_deleted_pods.txt'

# Prometheus query
thresold_value = '95'
QUERY = f'((sum (container_memory_working_set_bytes{{image!="",container!="POD", namespace=~"prod"}}) by (pod)) / (sum(kube_pod_container_resource_requests{{resource="memory", namespace=~"prod"}}) by (pod)) ) * 100 >= {thresold_value}'

# Function to query Prometheus
def query_promethous(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    data = response.json()
    # return data

    if data['status'] == 'success':
        return data['data']['result']
    else:
        print('Query failed')
        return None

def delete_pods(pods):
    # slack_client = WebClient(token=SLACK_TOKEN)
    with open(POD_FILE, 'w') as f:
        for pod in pods:
            print(f'Deleting pod {pod["metric"]["pod"]}')
            # f.write(f'{date} | {pod["metric"]["pod"]} Pod deleted\n')
            # requests.post(SLACK_WEBHOOK_URL, json={'text': f'Testing ignore Deleted pod {pod["metric"]["pod"]}'})
            exit_status = os.system(f'kubectl delete pod {pod["metric"]["pod"]} -n {namespace}')
            if exit_status == 0:
                f.write(f'{date} | {pod["metric"]["pod"]} Pod deleted\n')
                requests.post(SLACK_WEBHOOK_URL, json={'text': f'[Info Alert] | Memory utilization is high, above 95% | Pod {pod["metric"]["pod"]} Deleted in {namespace} namespace'})
            else:
                f.write(f'{date} | {pod["metric"]["pod"]} in {namespace} namespace Pod deletion failed\n')
                requests.post(SLACK_WEBHOOK_URL, json={'text': f'Failed to delete pod {pod["metric"]["pod"]}'})
            # slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=f'Deleted pod {pod["metric"]["pod"]}')

# Get the pods that match the query
pods = query_promethous(QUERY)
if pods is not None:
    print(f'Found {len(pods)} pods')
else:
    print('No pods found')

# Delete the pods
if pods is not None:
    delete_pods(pods)
