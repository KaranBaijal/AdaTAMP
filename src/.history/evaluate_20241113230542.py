import sys, os
import IPython.display
from sys import platform
from PIL import Image
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
import argparse
from openai import OpenAI
from task_planner import TaskPlanner
from vh_environment import VhEnv
import vh_utils as utils
sys.path.append(test)
from test.graph_verification import verify_graph_structure
from demo.utils_demo import *
from simulation.unity_simulator import comm_unity

# modify dir
YOUR_FILE_NAME = "/Users/zhiwenqiu/Documents/projects/AdaTAMP/virtualhome/simulation/macos_exec.v2.3.0.app"
comm = comm_unity.UnityCommunication(file_name=YOUR_FILE_NAME, port="8080", x_display="0")


class MockConfig:
    class Environment:
        observation_types = ['full']
        use_editor = True
        base_port = 8080
        port_id = 1
        executable_args = {'file_name': "/path/to/your/executable"}
        recording_options = {
            'recording': False,
            'output_folder': './output',
            'file_name_prefix': 'Test',
            'cameras': ['PERSON_FROM_BACK']
        }

    environment = Environment()


if __name__ == '__main__':
    openai_api_key = "your_openai_api_key_here"
    task_description = "sit on the sofa"

    # Generate the initial graph
    comm.reset(0)
    success, init_graph = comm.environment_graph()
    if not success:
        print("Failed to retrieve the initial environment graph.")
    
    # Start with a room-only graph
    init_graph = {
        "nodes": [
            {
                "id": 1,
                "class_name": "livingroom",
                "category": "Rooms",
                "obj_transform": {
                    "position": [0, 0, 0],
                    "rotation": [0, 0, 0, 1],
                    "scale": [1, 1, 1]
                }
            },
            {
                "id": 2,
                "class_name": "sofa",
                "category": "Furniture",
                "obj_transform": {
                    "position": [1, 0, 1],
                    "rotation": [0, 0, 0, 1],
                    "scale": [1, 1, 1]
                }
            }
        ],
        "edges": [
            {
                "from_id": 2,
                "to_id": 1,
                "relation_type": "INSIDE"
            }
        ]
    }

    print("Initial Graph for Debugging:")
    print(json.dumps(init_graph, indent=2))

    # Try expanding this minimal graph
    success, message = comm.expand_scene(init_graph)
    if not success:
        print(f"Failed to expand scene: {message}")
    else:
        print("Scene expanded successfully.")
    #     init_graph = {
    #         "nodes": [],
    #         "edges": []
    #     }

    # # Add a cat node linked to the sofa

    # sofa = [node for node in init_graph['nodes'] if node['class_name'] == 'sofa'][-1]
    # cat_node = {
    #         'class_name': 'cat',
    #         'category': 'Animals',
    #         'id': 1000,
    #         'properties': [],
    #         'states': [],
    #         'obj_transform': {'position': [1, 0, 1], 'rotation': [0, 0, 0, 1], 'scale': [1, 1, 1]}
    #     }
    # init_graph['nodes'].append(cat_node)
    # init_graph['edges'].append({'from_id': 1000, 'to_id': sofa['id'], 'relation_type': 'ON'})

    #  # Modify TV and light nodes' states
    # tv_node = next(node for node in init_graph['nodes'] if node['class_name'] == 'tv')
    # light_node = next(node for node in init_graph['nodes'] if node['class_name'] == 'lightswitch')
    # tv_node['states'] = ['ON']
    # light_node['states'] = ['OFF']

    # # Add a character node to the environment
    # character_node = {
    #         'id': 2000,
    #         'class_name': 'character',
    #         'category': 'Agents',
    #         'properties': [],
    #         'states': [],
    #         'obj_transform': {
    #             'position': [2, 0, 2],
    #             'rotation': [0, 0, 0, 1],
    #             'scale': [1, 1, 1]
    #         }
    # }
    # init_graph['nodes'].append(character_node)

    # verify graph nodes and edges
    verify_graph_structure(init_graph)

    # Create sample task_d for resetting the environment
    task_d = {
        'task_id': 1,
        'init_graph': init_graph,
        'init_room': 'living_room',
        'task_goal': {},
        'task_name': task_description,
        'env_id': 0
    }

    mock_cfg = MockConfig()

    # Initialize TaskPlanner
    planner = TaskPlanner(
        openai_api_key=openai_api_key,
        cfg=mock_cfg
    )

    # Reset the environment with the task details
    planner.env.reset(task_d)

    # Generate and print actions
    actions = planner.init_task_plan(task_description)
    print("Generated Task Plan:", actions)

    # Execute the plan and print the result
    success = planner.execute_plan(actions)
    if success:
        print("Task executed successfully.")
    else:
        print("Task execution failed.")