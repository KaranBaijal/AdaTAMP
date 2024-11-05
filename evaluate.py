from task_planner import TaskPlanner
from evaluator import Evaluator
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A simple main method with arguments")
    parser.add_argument('-k', '--key', type=str, help="Your OpenAI API key.")
    args = parser.parse_args()

    task_description = "clean the living room"
    planner = TaskPlanner(
        openai_api_key=args.key
    )
    evaluator = Evaluator()

    actions = planner.init_task_plan(task_description)
    print("Generated Task Plan:", actions)

    success = planner.execute_plan(actions)
    evaluator.evaluate_task({"success": success})
    evaluator.log_metrics()