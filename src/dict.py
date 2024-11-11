import json
import os

def load_dict(sim2nl_path='resource/wah_objects_sim2nl.json', nl2sim_path='resource/wah_objects_nl2sim.json'):
    with open(sim2nl_path, 'r') as file:
        obj_dict_sim2nl = json.load(file)
    with open(nl2sim_path, 'r') as file:
        obj_dict_nl2sim = json.load(file)
    return obj_dict_sim2nl, obj_dict_nl2sim