import sys, os
# add root path to avoid errors for __init__.py from vh
sys.path.insert(0, 'virtualhome')
import json
from openai import OpenAI
from src.vh_environment import VhEnv
import src.vh_utils as utils
from virtualhome.simulation.unity_simulator import comm_unity
import argparse
from jsonschema import validate, ValidationError

# # run directly
# from vh_environment import VhEnv
# import vh_utils as utils
# from dict import load_dict

# run .ipynb
from src.vh_environment import VhEnv
import src.vh_utils as utils
from src.dict import load_dict


class TaskPlanner:
    ACTION_SCHEMA = {
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

    def __init__(self, openai_api_key, cfg):
        self.client = OpenAI(api_key=openai_api_key)
        self.env = VhEnv(cfg)
        self.obj_dict_sim2nl, self.obj_dict_nl2sim = load_dict()
        self.comm = comm_unity.UnityCommunication()

    def init_prompt(self, task_description):
        env_description = self.describe_environment()

        schema_definition = {
            "type": "object",
            "properties": {
                "action_sequence": {
                    "type": "array",
                    "items": self.ACTION_SCHEMA
                }
            },
            "required": ["action_sequence"],
            "additionalProperties": False
        }

        # # two agents
        # prompt = (
        #     f"You are a high-level planner in the VirtualHome environment. The environment is described as follows: {env_description}. "
        #     f"Your task is to break down the task '{task_description}' into a sequence of structured actions that two virtual characters, 'char0' and 'char1', can execute cooperatively in this environment. "
        #     "Distribute the steps efficiently between the two characters to minimize redundant movements and ensure no two characters perform the same action on the same object simultaneously. "
        #     "Each action should include the character performing the action, the action itself, the target object, and the object ID. "
        #     "Return the actions strictly in JSON format as a list of dictionaries, with each dictionary containing keys 'character', 'action', 'object', and 'id'. "
        #     "Do not include any extra text or explanation, only JSON."
        #     "\n\nExample output:\n"
        #     "[\n"
        #     "  {\"character\": \"char0\", \"action\": \"Walk\", \"object\": \"cabinet\", \"id\": 123},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Open\", \"object\": \"cabinet\", \"id\": 123},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Grab\", \"object\": \"plate\", \"id\": 456},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Grab\", \"object\": \"cup\", \"id\": 789},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Walk\", \"object\": \"kitchen table\", \"id\": 111},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Walk\", \"object\": \"kitchen table\", \"id\": 111},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Place\", \"object\": \"plate\", \"id\": 456},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Place\", \"object\": \"cup\", \"id\": 789}\n"
        #     "]\n\n"
        #     f"Now, generate the actions for the task: '{task_description}'"
        # )
        # return prompt, schema_definition
    
        # # two agents with feedback
        # prompt = (
        #     f"You are a high-level planner in the VirtualHome environment. The environment is described as follows: {env_description}. "
        #     f"Your task is to break down the task 'please serve on the table: 1 cup of coffee, 1 glass of wine, 1 glass of juice and 1 apple (need to open fridge for juice)' into a sequence of structured actions that two virtual characters, 'char0' and 'char1', can execute cooperatively in this environment. "
        #     "Distribute the steps efficiently between the two characters to minimize redundant movements and ensure no two characters perform the same action on the same object simultaneously. "
        #     "Each action should include the character performing the action, the action itself, the target object, and the object ID. "
        #     "Return the actions strictly in JSON format as a list of dictionaries, with each dictionary containing keys 'character', 'action', 'object', and 'id'. "
        #     "Do not include any extra text or explanation, only JSON."
        #     "\n\nExample output:\n"
        #     "[\n"
        #     "  {\"character\": \"char0\", \"action\": \"Walk\", \"object\": \"cabinet\", \"id\": 123},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Open\", \"object\": \"cabinet\", \"id\": 123},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Grab\", \"object\": \"plate\", \"id\": 456},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Grab\", \"object\": \"cup\", \"id\": 789},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Walk\", \"object\": \"kitchen table\", \"id\": 111},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Walk\", \"object\": \"kitchen table\", \"id\": 111},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Place\", \"object\": \"plate\", \"id\": 456},\n"
        #     "  {\"character\": \"char1\", \"action\": \"Place\", \"object\": \"cup\", \"id\": 789}\n"
        #     "]\n\n"
        #     f"Now, generate the actions for the task: 'please serve on the table: 1 cup of coffee, 1 glass of wine, 1 glass of juice and 1 apple'"
        # )
        # return prompt, schema_definition

        
        # one agent
        prompt = (
            f"You are a high-level planner in the VirtualHome environment. The environment is described as follows: {env_description}. "
            f"Your task is to break down the task '{task_description}' into a sequence of structured actions that a virtual character can execute in this environment. "
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
        return prompt, schema_definition
    
        # # one agent with feedback
        # prompt = (
        #     f"You are a high-level planner in the VirtualHome environment. The environment is described as follows: {env_description}. "
        #     f"Your task is to break down the task 'Put 1 cupcake, 1 juice, 1 pound cake, and 1 pudding on the kitchen table. (need to find all snacks)' into a sequence of structured actions that a virtual character can execute in this environment. "
        #     "Each action should include the character performing the action, the action itself, the target object, and the object ID. "
        #     "Return the actions strictly in JSON format as a list of dictionaries, with each dictionary containing keys 'character', 'action', 'object', and 'id'. "
        #     "Do not include any extra text or explanation, only JSON."
        #     "\n\nExample output:\n"
        #     "[\n"
        #     "  {\"character\": \"char0\", \"action\": \"Walk\", \"object\": \"sofa\", \"id\": 123},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Grab\", \"object\": \"remote\", \"id\": 456},\n"
        #     "  {\"character\": \"char0\", \"action\": \"Sit\", \"object\": \"sofa\", \"id\": 123}\n"
        #     "]\n\n"
        #     f"Now, generate the actions for the task: 'Put 1 cupcake, 1 juice, 1 pound cake, and 1 pudding on the kitchen table.'"
        # )
        # return prompt, schema_definition
    
    def validate_response(self, response):
        schema_definition = {
            "type": "object",
            "properties": {
                "action_sequence": {
                    "type": "array",
                    "items": self.ACTION_SCHEMA
                }
            },
            "required": ["action_sequence"],
            "additionalProperties": False
        }
        try:
            validate(instance=response, schema=schema_definition)
            print("Response validation successful.")
            return True
        except ValidationError as e:
            print(f"Response validation failed: {e.message}")
            return False

    def init_task_plan(self, task_description):
        prompt, schema_definition = self.init_prompt(task_description)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a high-level planner for VirtualHome."},
                    {"role": "user", "content": prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "action_sequence_schema",
                        "schema": schema_definition
                    }
                },
                max_tokens=300,
                temperature=0
            )
            response_content = json.loads(response.choices[0].message.content)

            if not self.validate_response(response_content):
                print("Invalid response. Aborting.")
                return []

            actions = response_content["action_sequence"]
            print("Generated Actions:", actions)
            return actions

        except json.JSONDecodeError:
            print("Error: Response was not in expected JSON format.")
        except KeyError:
            print("Error: Response missing 'action_sequence'.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return []

    def process_response(self, response_text):
        """
        Converts the response text into a Python dictionary.
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("Error: Response was not in expected JSON format.")
            raise
    
    def describe_environment(self):
        graph = self.env.get_graph()
        description = []

        for node in graph['nodes']:
            node_desc = f"{node['class_name']} with ID {node['id']}"
            if 'properties' in node:
                node_desc += f" having properties {', '.join(node['properties'])}"
            description.append(node_desc)

        for edge in graph['edges']:
            relation = edge.get('relation', 'UNKNOWN_RELATION')
            edge_desc = f"There is a connection from {edge['from_id']} to {edge['to_id']} with relation {relation}"
            description.append(edge_desc)

        return " ".join(description)
    
    # def init_skill_set(self):
    #     self.skills = ["Walk", "Grab", "Open", "Close", "PutIn", "PutBack", "SwitchOn", "SwitchOff"]
    #     print(f"Available skills: {self.skills}")

    # execute plan for baseline
    def execute_plan(self, actions):
        for action in actions:
            try:
                step_scripts = utils.step_nl2sim(
                    action['action'],
                    self.obj_dict_nl2sim,
                    action['object']
                )

                if not isinstance(step_scripts, list):
                    step_scripts = [step_scripts]

                for step_script in step_scripts:
                    print(f"Executing step: {step_script}")
                    success, message = self.comm.render_script(
                        script=[step_script],
                        processing_time_limit=60,
                        find_solution=False,
                        image_width=320,
                        image_height=240,
                        skip_animation=False,
                        recording=True,
                        save_pose_data=True,
                        file_name_prefix="task_execution"
                    )
                    if not success:
                        print(f"Execution failed: {message}")
                        return False
            except Exception as e:
                print(f"Error during step execution: {e}")
                return False
        return True
    
    
    # # execute_plan for adding motion planning
    # def execute_plan(self, actions):
    #     for action in actions:
    #         try:
    #             if action['action'].lower() == 'walk':
    #                 # Plan a path to the target object
    #                 path = self.env.calculate_path_to_object(action['object'])
    #                 for step in path:
    #                     print(f"Executing path step: {step}")
    #                     success, message = self.env.comm.render_script([step], find_solution=False)
    #                     if not success:
    #                         print(f"Path execution failed: {message}")
    #                         return False

    #             # Translate and execute the action
    #             step_script = utils.step_nl2sim(
    #                 action['action'],
    #                 self.obj_dict_nl2sim,
    #                 action['object']
    #             )
    #             print(f"Executing step: {step_script}")
    #             success, message = self.env.comm.render_script(
    #                 script=[step_script],
    #                 find_solution=False
    #             )
    #             if not success:
    #                 print(f"Execution failed: {message}")
    #                 return False

    #         except Exception as e:
    #             print(f"Error during step execution: {e}")
    #             return False
    #     return True