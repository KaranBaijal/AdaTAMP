import sys
import os
import copy
import random
import math
import json

# # run directly
# from dict import load_dict

# run .ipynb
from src.dict import load_dict


# Use most of the functions in this github repo: https://github.com/lbaa2022/LLMTaskPlanning
def separate_new_ids_graph(graph, max_id):
    new_graph = copy.deepcopy(graph)
    for node in new_graph['nodes']:
        if node['id'] > max_id:
            node['id'] = node['id'] - max_id + 1000
    for edge in new_graph['edges']:
        if edge['from_id'] > max_id:
            edge['from_id'] = edge['from_id'] - max_id + 1000
        if edge['to_id'] > max_id:
            edge['to_id'] = edge['to_id'] - max_id + 1000
    return new_graph

# extract natural language instructions (e.g., put down the book) to executable script in vh
def step_nl2sim(step_nl, obj_dict_nl2sim, target_object, resource_folder='resource'):
    print(f"Received step_nl: {step_nl}")
    obj_dict_sim2nl, obj_dict_nl2sim = load_dict()

    # Normalize step to ensure consistent matching
    step_nl_normalized = step_nl.strip().lower()

    if step_nl_normalized == "walk":
        if target_object in obj_dict_nl2sim:
            target_sim = obj_dict_nl2sim[target_object]

            if "room" in target_object.lower():
                graph = self.get_graph()
                doors = [node for node in graph["nodes"] if node["class_name"] == "door"]
                connected_doors = [
                    door for door in doors
                    if any(edge["from_id"] == door["id"] and edge["to_id"] == obj_dict_nl2sim[target_object] for edge in graph["edges"])
                ]

                if not connected_doors:
                    raise ValueError(f"No door found connected to the room '{target_object}'. Check graph relationships.")

                door_sim = connected_doors[0]["id"]

                script = [
                    f"<char0> [walk] <{door_sim}> (1)", 
                    f"<char0> [open] <{door_sim}> (1)",  
                    f"<char0> [walk] <{target_sim}> (1)" 
                ]
            else:
                script = [f"<char0> [walk] <{target_sim}> (1)"]
        else:
            raise ValueError(f"Target object '{target_object}' not found in object dictionary.")

    elif step_nl_normalized in ["grab", "open", "close", "look", "switchon", "switchoff"]:
        action = step_nl_normalized
        obj_sim = obj_dict_nl2sim.get(target_object)
        if not obj_sim:
            raise ValueError(f"Object '{target_object}' not found in object dictionary.")
        script = [f"<char0> [{action}] <{obj_sim}> (1)"]

    else:
        raise NotImplementedError(f"Step '{step_nl}' is not supported.")

    print(f"Translated step '{step_nl}' to script(s): {script}")
    return script


def split_step_sim(step_sim, with_ids=False):
    step_elements = step_sim.split(' ')
    act = step_elements[1].replace('[','').replace(']','')
    obj1_name = step_elements[2].replace('<','').replace('>','')
    if with_ids == False:
        if len(step_elements)==4:
            return act, obj1_name
        elif len(step_elements)==6:
            obj2_name = step_elements[4].replace('<','').replace('>','')
            return act, obj1_name, obj2_name
        else:
            raise NotImplementedError
    else:
        if len(step_elements)==4:
            return act, obj1_name, int(step_elements[3].replace('(','').replace(')',''))
        elif len(step_elements)==6:
            obj2_name = step_elements[4].replace('<','').replace('>','')
            return act, obj1_name, int(step_elements[3].replace('(','').replace(')','')), obj2_name, int(step_elements[5].replace('(','').replace(')',''))
        else:
            raise NotImplementedError

    
def change_step_sim_obj_ids(step_sim, obj_ids):
    if len(obj_ids) == 1:
        return f"{step_sim.split('(')[0]}({obj_ids[0]})"
    elif len(obj_ids) == 2:
        return f"{step_sim.split('(')[0]}({obj_ids[0]}){step_sim.split(')')[1].split('(')[0]}({obj_ids[1]})"
    else:
        raise NotImplementedError
    
def find_indefinite_article(w):
    # simple rule, not always correct
    w = w.lower()
    if w[0] in ['a', 'e', 'i', 'o', 'u']:
        return 'an'
    else:
        return 'a'

def get_ids_by_class_name(graph, class_name):
    return [node['id'] for node in graph['nodes'] if node['class_name'] == class_name]

def euclidean_dist(pos1, pos2):
    distance = 0
    for i in range(len(pos1)):
        distance += (pos1[i]-pos2[i])**2
    return math.sqrt(distance)

def select_obj_id(graph, obj_ids, method="distance"):
    id2nodes = {node['id']: node for node in graph['nodes']}
    if method == "distance":
        agent_ids = get_ids_by_class_name(graph, "character")
        if len(agent_ids) == 1:
            agent_id = agent_ids[0]
            agent_position = id2nodes[agent_id]['obj_transform']['position']
        else:
            raise NotImplementedError
        min_dist = 1e3
        for obj_id in obj_ids:
            if euclidean_dist(agent_position, id2nodes[obj_id]['obj_transform']['position']) < min_dist:
                selected_obj_id = obj_id
    else:
        raise NotImplementedError
    return selected_obj_id

def get_related_edges_by_id(graph, id):
    edges_from_id = [edge for edge in graph['edges'] if edge['from_id']==id]
    edges_to_id = [edge for edge in graph['edges'] if edge['to_id']==id]
    return edges_from_id, edges_to_id

def get_location_info_by_id(graph, node_id):
    id2node = {node['id']: node for node in graph['nodes']}
    edges_from_id, _ = get_related_edges_by_id(graph, node_id)
    room_node_ids, in_recepticle_ids, on_recepticle_ids = [], [], []
    for related_edge in edges_from_id:
        to_obj_id = related_edge['to_id']
        if related_edge['relation_type'] == 'INSIDE':
            if id2node[to_obj_id]['category'] == 'Rooms':
                room_node_ids.append(to_obj_id)
            else:
                in_recepticle_ids.append(to_obj_id)
        elif related_edge['relation_type'] == 'ON':
            on_recepticle_ids.append(to_obj_id)
    obj_location = {'room_node_ids': room_node_ids,
                    'in_recepticle_ids': in_recepticle_ids,
                    'on_recepticle_ids': on_recepticle_ids}
    return obj_location

def check_node_is_state(node, state):
    return state in node['states']

def check_node_is_close_to_agent(graph, agent_id, obj_id):
    edges_from_obj, edges_to_obj = get_related_edges_by_id(graph, obj_id)
    return agent_id in [edge['to_id'] for edge in edges_from_obj]

def check_in_recep_is_open(graph, obj_id):
    id2node = {node['id']: node for node in graph['nodes']}
    obj_in_recep_ids = get_location_info_by_id(graph, obj_id)['in_recepticle_ids']
    if len(obj_in_recep_ids) == 0:
        return True, None
    elif len(obj_in_recep_ids) == 1:
        if not check_node_is_state(id2node[obj_in_recep_ids[0]], 'CLOSED'):
            return True, None
        else:
            return False, obj_in_recep_ids[0] 
    else:
        raise NotImplementedError

def check_free_hand(graph, agent_id):
    edges_from_obj, edges_to_obj = get_related_edges_by_id(graph, agent_id)
    grabbed_objs = [edge_from_obj['to_id'] for edge_from_obj in edges_from_obj if 'HOLDS' in edge_from_obj['relation_type']]
    return len(grabbed_objs) < 2

def check_holding_obj(graph, agent_id, obj_id):
    edges_from_obj, edges_to_obj = get_related_edges_by_id(graph, agent_id)
    x =  [edge_from_obj['relation_type'] for edge_from_obj in edges_from_obj if edge_from_obj['to_id']==obj_id]
    return 'HOLDS_RH' in x or 'HOLDS_LH' in x

def check_goal_condition(graph, task_goal):
    # task_goal keys -> 'inside_X_Y' 'on_X_Y' 'turnOn_X'
    id2node = {node['id']: node for node in graph['nodes']}
    task_goal_first_key = next(iter(task_goal))
    to_obj_name = task_goal_first_key.split('_')[-1]
    to_obj_ids = get_ids_by_class_name(graph, to_obj_name)
    
    final_state_candi = {}
    for to_obj_id in to_obj_ids:
        final_state = {}
        for goal_key, goal_n in task_goal.items():
            if 'turnOn' in goal_key:
                relation, _ = goal_key.split('_')
                states = id2node[to_obj_id]['states']
                if 'ON' in states:
                    final_state[goal_key] = (1, goal_n)
                else:
                    final_state[goal_key] = (0, goal_n)
            elif 'on' in goal_key or 'inside' in goal_key:
                relation, from_obj_name, _ = goal_key.split('_')
                _, edges_to_id = get_related_edges_by_id(graph, to_obj_id)
                count_satisfied = 0
                for edge in edges_to_id:
                    if id2node[edge['from_id']]['class_name'] == from_obj_name and relation == edge['relation_type'].lower():
                        count_satisfied += 1
                final_state[goal_key] = (count_satisfied, goal_n)
        final_state_candi[to_obj_id] = final_state
    
    
    scores = {to_obj_id: score_accomplish(final_state) for to_obj_id, final_state in final_state_candi.items()}
    max_score = max(scores.values())
    max_key = [key for key, value in scores.items() if value == max_score]
    # pdb.set_trace()
    return max_key[0], final_state_candi[max_key[0]]

def score_accomplish(final_state):
    # final_state example: {'on_juice_coffeetable': (0, 1), 'on_wine_coffeetable': (0, 1), 'on_pudding_coffeetable': (0, 1)}
    score = 0
    for k, v in final_state.items():
        score += min(v[0], v[1])/v[1]
    return score


def divide_total_into_keys(keys, total):
    if not keys or total <= 0:
        return {}

    num_keys = len(keys)
    value_per_key = total // num_keys
    remainder = total % num_keys

    result_dict = {}
    for i, key in enumerate(keys):
        value = value_per_key + 1 if i < remainder else value_per_key
        result_dict[key] = value

    return result_dict
