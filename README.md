# cleanup-scheduled-triggers

This repo contains a script that deletes all scheduled events that have a webhook URL set to a specific value. This is useful when you want to clean up all scheduled events that were created for a specific webhook URL.

## Requirements

- Python 3
- Requests library (`pip3 install requests`)

## Setup

1. Download the file `delete_scheduled_event.py` from this gist.
2. Install the required libraries using pip:

     ```bash
     pip3 install requests
     ```

## Usage

1. Set up environment variables.

   - `HASURA_ADMIN_SECRET`: The admin secret for accessing the API endpoint.
   - `HASURA_GRAPHQL_ENGINE_BASE_URL`:  The hostname of the API endpoint (e.g., if your graphql endpoint is `https://capital-elk-82.hasura.app/v1/graphql`, the value here will be `https://capital-elk-82.hasura.app`)
   - `WEBHOOK_URL`: Tpt fetches scheduled events in batches from the `/v1/metadata` endpoint.
- It filters events with the `webhook_conf` value as the set `WEBHOOK_URL` environment variable and deletes them using their IDs.

## Notes

- Ensure there are no white spaces in the environment variables

