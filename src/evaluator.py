class Evaluator:
    def __init__(self):
        self.total_tasks = 0
        self.successful_tasks = 0
        self.failed_tasks = 0

    def evaluate_task(self, task_result):
        self.total_tasks += 1
        if task_result["success"]:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1

    def calculate_metrics(self):
        success_rate = (self.successful_tasks / self.total_tasks) * 100 if self.total_tasks else 0
        failure_rate = (self.failed_tasks / self.total_tasks) * 100 if self.total_tasks else 0

        metrics = {
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "total_tasks": self.total_tasks,
            "successful_tasks": self.successful_tasks,
            "failed_tasks": self.failed_tasks
        }
        return metrics

    def log_metrics(self):
        metrics = self.calculate_metrics()
        print("Evaluation Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")