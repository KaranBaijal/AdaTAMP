import json

def load_tasks(task_file):
    with open(task_file, "r") as file:
        return json.load(file)

def construct_easy_tasks(single_step_descriptions, start_id=1000):
    tasks = []
    for i, description in enumerate(single_step_descriptions):
        task_id = start_id + i
        task = {
            "task_id": task_id,
            "task_name": "find",
            "nl_instructions": [description],
            "task_plan": [description]
        }
        tasks.append(task)
    return tasks

def categorize_tasks(tasks):
    categorized_tasks = {"Easy": [], "Medium": [], "Hard": []}

    for task in tasks:
        num_steps = len(task.get("task_plan", []))

        if num_steps <= 3:
            category = "Easy"
        elif 4 <= num_steps <= 10:
            category = "Medium"
        else:
            category = "Hard"

        categorized_tasks[category].append(task)

    return categorized_tasks

def save_tasks(sorted_tasks, output_file):
    with open(output_file, "w") as file:
        json.dump(sorted_tasks, file, indent=4)

def main():
    input_file = "/Users/zhiwenqiu/Documents/projects/AdaTAMP/resource/task_examples.json"
    output_file = "/Users/zhiwenqiu/Documents/projects/AdaTAMP/resource/sorted_tasks.json"

    # List of single-step task descriptions
    single_step_descriptions = [
        "find a wine glass",
        "find a coffee table",
        "find a water glass",
        "find a dishwasher",
        "find a fridge",
        "find a coffee table",
        "find a plate",
        "find a wine",
        "find a cabinet",
        "find a juice",
        "find an apple",
        "find a pudding"
    ]

    print("Loading tasks...")
    tasks = load_tasks(input_file)

    print("Constructing new single-step 'find' tasks...")
    new_tasks = construct_easy_tasks(single_step_descriptions, start_id=1000)

    print("Adding new tasks to the task library...")
    tasks.extend(new_tasks)

    print("Categorizing tasks by complexity...")
    sorted_tasks = categorize_tasks(tasks)

    print("Saving sorted tasks to file...")
    save_tasks(sorted_tasks, output_file)

    print("Tasks sorted and saved successfully!")

if __name__ == "__main__":
    main()