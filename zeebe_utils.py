import json
import os

import grpc
import requests
from dotenv import load_dotenv
from zeebe_grpc import gateway_pb2_grpc, gateway_pb2
from google.protobuf.json_format import MessageToDict

from auth_gateway import AuthGateway

load_dotenv()


async def get_zeebe_access_token():
    ZEEBE_CLIENT_ID = os.environ["ZEEBE_CLIENT_ID"]
    ZEEBE_CLIENT_SECRET = os.environ["ZEEBE_CLIENT_SECRET"]
    ZEEBE_AUTHORIZATION_SERVER_URL = os.environ["ZEEBE_AUTHORIZATION_SERVER_URL"]

    token_data = {
        "grant_type": "client_credentials",
        "client_id": ZEEBE_CLIENT_ID,
        "client_secret": ZEEBE_CLIENT_SECRET,
        "audience": "zeebe.camunda.io"
    }

    # Get access token
    response = requests.post(ZEEBE_AUTHORIZATION_SERVER_URL, data=token_data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")

        return access_token


async def get_zeebe_client():
    ZEEBE_ADDRESS = os.environ["ZEEBE_ADDRESS"]
    access_token = await get_zeebe_access_token()

    # Create a Camunda 8 cloud channel
    call_creds = grpc.access_token_call_credentials(access_token)
    channel_creds = grpc.ssl_channel_credentials()
    composite_creds = grpc.composite_channel_credentials(channel_creds, call_creds)
    channel = grpc.secure_channel(ZEEBE_ADDRESS, credentials=composite_creds)

    # Create a stub to interact with the Zeebe gRPC service
    zeebe_client = gateway_pb2_grpc.GatewayStub(channel)

    return zeebe_client


async def run_process_with_result():
    zeebe_client = await get_zeebe_client()
    variables = {"instanceId": 12345}

    process_instance = zeebe_client.CreateProcessInstance(
        gateway_pb2.CreateProcessInstanceRequest(
            bpmnProcessId="get-current-version-testing",
            version=-1,
            variables=json.dumps(variables)
        )
    )

    result = {
        "processDefinitionKey": process_instance.processDefinitionKey,
        "bpmnProcessId": process_instance.bpmnProcessId,
        "version": process_instance.version,
        "processInstanceKey": process_instance.processInstanceKey
    }
    return result


async def get_topology():
    zeebe_client = await get_zeebe_client()
    topology = zeebe_client.Topology(gateway_pb2.TopologyRequest())

    return topology



