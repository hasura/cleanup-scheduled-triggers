import os
import requests
import time

base_url = os.getenv("HASURA_GRAPHQL_ENGINE_BASE_URL")
hasura_role = "admin"
hasura_admin_secret = os.getenv("HASURA_ADMIN_SECRET")
webhook_url = os.getenv("WEBHOOK_URL")


# Function to fetch scheduled events
def get_scheduled_events(limit=10, offset=0):
    url = f"{base_url}/v1/metadata"
    payload = {
        "type": "get_scheduled_events",
        "args": {
            "type": "one_off",
            "limit": limit,
            "offset": offset,
            "status": ["scheduled"],
        },
    }
    headers = {
        "X-Hasura-Role": hasura_role,
        "x-hasura-admin-secret": hasura_admin_secret,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 429:  # Rate limit status code
            print("Rate limit exceeded. Sleeping for 10 seconds.")
            time.sleep(10)
            return None
        response.raise_for_status()  # Check for 200 status code
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request exception occurred: {err}")
        return None


# Function to delete scheduled events
def delete_scheduled_event(event_id):
    url = f"{base_url}/v1/metadata"
    payload = {
        "type": "delete_scheduled_event",
        "args": {"type": "one_off", "event_id": event_id},
    }
    headers = {
        "X-Hasura-Role": hasura_role,
        "x-hasura-admin-secret": hasura_admin_secret,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 429:  # Rate limit status code
            print("Rate limit exceeded. Sleeping for 10 seconds.")
            time.sleep(10)
            return None
        response.raise_for_status()  # Check for 200 status code
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request exception occurred: {err}")
        return None


offset = 0
limit = 100
deleted_count = 0

while True:
    scheduled_events_response = get_scheduled_events(limit, offset)
    if scheduled_events_response is None:
        continue  # Skip to the next iteration if rate limit is exceeded or error occurred

    events = scheduled_events_response.get("events", [])

    event_ids_to_delete = [
        event["id"]
        for event in events
        if event.get("status") == "scheduled"
        and event.get("webhook_conf") == webhook_url
    ]

    if event_ids_to_delete:
        for event_id in event_ids_to_delete:
            delete_response = delete_scheduled_event(event_id)
            if delete_response is not None:
                deleted_count += 1
                print(f"Deleted event with ID {event_id}: {delete_response}")

    offset += limit - len(event_ids_to_delete)
    if len(events) < limit:
        break

print(f"Total deleted events: {deleted_count}")
