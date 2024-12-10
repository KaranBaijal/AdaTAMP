#!/Users/zhiwenqiu/opt/anaconda3/envs/zhiwen-project/bin/python
import sys, os
from sys import platform
import subprocess
print("Python executable:", sys.executable)

from PIL import Image
import json
import jsonschema
import matplotlib.pyplot as plt
from tqdm import tqdm
import argparse
from openai import OpenAI
from src.task_planner import TaskPlanner
from src.vh_environment import VhEnv
import src.vh_utils as utils
from src.tests.graph_verification import verify_graph_structure
from virtualhome.simulation.unity_simulator import comm_unity
from virtualhome.demo.utils_demo import *


# modify dir
YOUR_FILE_NAME = "/Users/zhiwenqiu/Documents/projects/AdaTAMP/virtualhome/simulation/macos_exec.2.2.4.app"
comm = comm_unity.UnityCommunication(file_name=YOUR_FILE_NAME, port="8080", x_display="0")

class MockConfig:
    class Environment:
        observation_types = ['full']
        use_editor = True
        base_port = 8080
        port_id = 1
        executable_args = {'file_name': "/Users/zhiwenqiu/Documents/projects/AdaTAMP/virtualhome/macos_exec.2.2.4.app"}
        recording_options = {
            'recording': False,
            'output_folder': './output',
            'file_name_prefix': 'Test',
            'cameras': ['PERSON_FROM_BACK']
        }

    environment = Environment()

action_sequence_schema = {
    "type": "object",
    "properties": {
        "action_sequence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "action": {"type": "string"},
                    "object": {"type": "string"},
                    "id": {"type": "integer"}
                },
                "required": ["character", "action", "object", "id"],
                "additionalProperties": False
            }
        }
    },
    "required": ["action_sequence"],
    "additionalProperties": False
}

def validate_response(response):
    try:
        jsonschema.validate(instance=response, schema=action_sequence_schema)
        print("Validation successful!")
        return True
    except jsonschema.ValidationError as e:
        print("Validation Error:", e.message)
        return False

if __name__ == '__main__':
    #openai_api_key = "your_openai_api_key_here"
    openai_api_key = "REMOVED_API_KEY"
    
    # modify to run all tasks
    task_description = "Put 1 cupcake, 1 juice, 1 pound cake, and 1 pudding on the kitchen table"

    # Generate the initial graph
    comm.reset(0)
    success, init_graph = comm.environment_graph()
    if not success:
        print("Failed to retrieve the initial environment graph.")
    
    # Define a simple initial graph
    init_graph = {
        "nodes": [
            {
                "id": 1,
                "class_name": "kitchen",
                "category": "Rooms",
                "obj_transform": {
                    "position": [0, 0, 0],
                    "rotation": [0, 0, 0, 1],
                    "scale": [1, 1, 1]
                },
                "properties": [],
                "states": []
            },
            {
                "id": 227,
                "class_name": "door",
                "category": "Doors",
                "obj_transform": {
                    "position": [0, 0, 1],
                    "rotation": [0, 0, 0, 1],
                    "scale": [1, 1, 1]
                },
                "properties": ["CAN_OPEN"],
                "states": ["CLOSED"]
            }
        ],
        "edges": [
            {
                "from_id": 227,
                "to_id": 1,
                "relation": "CONNECTED_TO"
            }
        ]
    }

    # print("Initial Graph for Debugging:")
    # print(json.dumps(init_graph, indent=2))

    # Verify graph nodes and edges
    # verify_graph_structure(init_graph)

    task_d = {
        'task_id': 1,
        'init_graph': init_graph,
        'init_room': 'kitchen',
        'task_goal': {},
        'task_name': task_description,
        'env_id': 0
    }

    mock_cfg = MockConfig()
    planner = TaskPlanner(
            openai_api_key=openai_api_key,
            cfg=mock_cfg
        )
    planner.env.reset(task_d)

    actions = planner.init_task_plan(task_description)
    # print("Generated Task Plan:", actions)

    if validate_response({"action_sequence": actions}):
        print("Actions are valid. Proceeding with execution...")
        success = planner.execute_plan(actions)
        if success:
            print("Task executed successfully!")
        else:
            print("Task execution failed.")
    else:
        print("Invalid action sequence. Aborting execution.")