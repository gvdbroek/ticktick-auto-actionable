import json
import logging
import os
import sys
import time
import requests

log_handlers = [logging.StreamHandler(sys.stdout)]

try:
    import dotenv
    logging.basicConfig(level=logging.INFO, handlers=log_handlers)
    dotenv.load_dotenv()
    logging.info("dotenv loaded token")
except ImportError:
    logging.basicConfig(handlers=log_handlers)
    logging.info("dotenv token not loaded, running in gcloud")
#
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
BASE_URL="https://api.ticktick.com"
REQUIRED_TAGS=["next"]
NEW_TASK_SORTORDER=100
NEW_TASK_PRIORITY=5
PROJECT_BLACKLIST=[] # should contain project NAMES 
NEW_TASK_MESSAGE= os.getenv("TASK_MSG", "Set #next action for:")


def generate_request_headers():
    token = os.getenv("API_KEY")
    return {
        "Authorization" : f"Bearer {token}"
    }

def request_projects():
    logging.info("requesting projects")
    endpoint = "/open/v1/project"
    return requests.get(BASE_URL + endpoint, headers=generate_request_headers()).json()

def request_project_data(project_id):
    logging.debug("requesting project %s data" % project_id)
    endpoint = f"/open/v1/project/{project_id}/data"
    return requests.get(BASE_URL + endpoint, headers=generate_request_headers()).json()


def is_actionable(project_data):
    if not 'tasks' in project_data:
        return False

    tasks = project_data['tasks']
    for task in tasks:
        task_title = task["title"]
        logging.info(f"-- {task_title}")

        if task['status'] != 0:
            continue

        if not 'tags' in task:
            continue
        task_tags = task['tags']

        if not task_tags:
            continue

        if all( required_tag in task_tags for required_tag in REQUIRED_TAGS):
            logging.info(f"vv {task_title}")
            return True

    return False

def create_actionable_task(project_data):
    # todo
    project_name = project_data['project']['name']
    project_id = project_data['project']['id']
    new_task = dict(
        title= NEW_TASK_MESSAGE + f" {project_name}",
        projectId=project_id,
        content="All projects are required to be actionable",
        isAllDay=True,
        priority=NEW_TASK_PRIORITY,
        sortOrder=NEW_TASK_PRIORITY,
        tags=REQUIRED_TAGS
    )
    endpoint = f"/open/v1/task"
    resp = requests.post(BASE_URL + endpoint, headers=generate_request_headers(), json=new_task)
    resp_data = resp.json()
    logging.debug(resp_data)
    if resp.status_code != 200:
        raise Exception("Failed to create new task: %s" % resp_data)



# Define main script
def main():
    """Program that simulates work using the sleep method and random failures.

    Args:
        sleep_ms: number of milliseconds to sleep
        fail_rate: rate of simulated errors
    """
    print(f"Starting Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    # Simulate work by waiting for a specific amount of time

    from pprint import pp
    
    projects = request_projects()
    for project in projects:
        project_id = project["id"]
        project_name= project["name"]
        logging.info(f"Checking task list {project_name} w/ id: {project_id}")

        if project['name'] in PROJECT_BLACKLIST:
            logging.info(f"-- Project task list {project_name} w/ id: {project_id} is in blacklist")
            continue

        data = request_project_data(project['id'])
        if is_actionable(data):
            continue
        logging.info(f"XX Missing #next tag in {project_name}")
        create_actionable_task(data)

    print(f"Completed Task #{TASK_INDEX}.")




# Start script
if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process
