import json
from Levenshtein import distance as levenshtein_distance

class TaskEvaluator:
    def __init__(self, ground_truth_steps, generated_steps):
        self.ground_truth_steps = ground_truth_steps
        self.generated_steps = generated_steps

    def compute_levenshtein_distance(self):
        ground_truth = " ".join([" ".join(step.split()[:2]) for step in self.ground_truth_steps])
        generated = " ".join([f"{action['action']} {action['object']}" for action in self.generated_steps])
        return levenshtein_distance(ground_truth, generated)

    def compute_action_order_deviation(self):
        ground_truth = [" ".join(step.split()[:2]) for step in self.ground_truth_steps]
        generated = [f"{action['action']} {action['object']}" for action in self.generated_steps]

        matched_indices = [generated.index(gt) for gt in ground_truth if gt in generated]
        if not matched_indices:
            return len(ground_truth)  # Full deviation if no matches

        deviations = sum(1 for i in range(len(matched_indices) - 1) if matched_indices[i] > matched_indices[i + 1])
        return deviations

    def compute_action_count_efficiency(self):
        ground_truth_len = len(self.ground_truth_steps)
        generated_len = len(self.generated_steps)
        return ground_truth_len / generated_len if generated_len > 0 else 0

    def compute_final_success_rate(self):
        ground_truth = [" ".join(step.split()[:2]) for step in self.ground_truth_steps]
        generated = [f"{action['action']} {action['object']}" for action in self.generated_steps]
        return int(all(gt in generated for gt in ground_truth))

    def compute_subgoal_success_rate(self):
        ground_truth = [" ".join(step.split()[:2]) for step in self.ground_truth_steps]
        generated = [f"{action['action']} {action['object']}" for action in self.generated_steps]
        matched_steps = len([gt for gt in ground_truth if gt in generated])
        return matched_steps / len(ground_truth) if ground_truth else 0

    def evaluate(self):
        return {
            "Levenshtein Distance": self.compute_levenshtein_distance(),
            "Action Order Deviation": self.compute_action_order_deviation(),
            "Action Count Efficiency": self.compute_action_count_efficiency(),
            "Final Success Rate": self.compute_final_success_rate(),
            "Subgoal Success Rate": self.compute_subgoal_success_rate()
        }