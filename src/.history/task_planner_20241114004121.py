import sys, os
# add root path to avoid errors for __init__.py from vh
sys.path.insert(0, '/Users/zhiwenqiu/Documents/projects/AdaTAMP/virtualhome')
import json
from openai import OpenAI
from vh_environment import VhEnv
import vh_utils as utils
from simulation.unity_simulator import comm_unity
import argparse

# # run directly
# from vh_environment import VhEnv
# import vh_utils as utils
# from dict import load_dict

# run .ipynb
from vh_environment import VhEnv
import vh_utils as utils
from dict import load_dict


class TaskPlanner:
    def __init__(self, openai_api_key, cfg):
        self.client = OpenAI(api_key=openai_api_key)
        self.env = VhEnv(cfg)
        self.obj_dict_sim2nl, self.obj_dict_nl2sim = load_dict()
        self.comm = comm_unity.UnityCommunication()
    
    # generate a structured task plan output from high-level descriptions 
    def init_task_plan(self, task_description):
        prompt, action_schema = self.init_prompt(task_description)
        response = self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a high-level planner for VirtualHome."},
                {"role": "user", "content": prompt}
            ],
            response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "action_sequence",
                "schema": {
                    "type": "array",
                    "items": action_schema
                },
                "strict": True
            }
            },
            max_tokens=300,
            temperature=0
        )
        actions = self.process_response(response.choices[0].message.content)
        return actions


 ## give image of scene or env graph representation, more in-context examples
  # TODO: Check with calvin abt environment_description
    def init_prompt(self, task_description):
        action_schema = {
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
        prompt = (
        f"You are a high-level planner in the VirtualHome environment. An evironment graph of where you are is {self.env}. \
        Your task is to break down the task '{task_description}' into a sequence of structured actions that a virtual character can execute in this environment graph. "
        "Each action should include the character performing the action, the action itself, the target object, and the object ID. "
        "Return the actions strictly in JSON format as a list of dictionaries, with each dictionary containing keys 'character', 'action', 'object', and 'id'. "
        "Do not include any extra text or explanation, only JSON."
        "\n\nExample output:\n"
        "[\n"
        "  {\"character\": \"char0\", \"action\": \"Walk\", \"object\": \"sofa\", \"id\": 123},\n"
        "  {\"character\": \"char0\", \"action\": \"Grab\", \"object\": \"remote\", \"id\": 456},\n"
        "  {\"character\": \"char0\", \"action\": \"Sit\", \"object\": \"sofa\", \"id\": 123}\n"
        "]\n\n"
        f"Now, generate the actions for the task: '{task_description}'"
    )
        return prompt, action_schema

    # convert json into structured actions
    def process_response(self, response_text):
        try:
            actions = json.loads(response_text)
            return actions
        except json.JSONDecodeError:
            print("Error: Response was not in expected JSON format.")
        return []

    def execute_plan(self, actions):
        # Convert high-level actions to simulation steps
        script = [
            utils.step_nl2sim(action['action'], self.obj_dict_nl2sim, None)  # Adjust parameters as needed
            for action in actions
        ]
        success, message = self.comm.render_script(
            script=script,
            processing_time_limit=60,
            find_solution=False,
            image_width=320,
            image_height=240,
            skip_animation=False,
            recording=True,
            save_pose_data=True,
            file_name_prefix="task_execution"
        )

        if success:
            print("Task executed successfully in VirtualHome.")
        else:
            print("Execution failed:", message)

# add reset, init_skill_set, score etc. if necessary for adapting to new env