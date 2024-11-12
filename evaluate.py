import sys, os
# sys.path.append(os.path.abspath('/Users/zhiwenqiu/Documents/projects/AdaTAMP/src'))

import IPython.display
from sys import platform
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import argparse
from openai import OpenAI
from src.task_planner import TaskPlanner
from src.vh_environment import VhEnv
import src.vh_utils as utils
from virtualhome.demo.utils_demo import *
from virtualhome.simulation.unity_simulator import comm_unity

# modify dir
YOUR_FILE_NAME = "/Users/zhiwenqiu/Documents/projects/AdaTAMP/virtualhome/simulation/macos_exec.2.2.4.app"
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
    openai_api_key = "your_openai_api_key_here"  # Replace with your actual API key
    task_description = "sit on the sofa"
    task_d = {
        'task_id': 1,
        'init_graph': {},  # Provide a valid initial graph if needed
        'init_room': 'living_room',
        'task_goal': {},  # Define task goal if necessary
        'task_name': task_description,
        'env_id': 0
    }

    mock_cfg = MockConfig()

    # Initialize TaskPlanner
    planner = TaskPlanner(
        openai_api_key=openai_api_key,
        cfg=mock_cfg
    )

    # Explicitly reset the environment with task details
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