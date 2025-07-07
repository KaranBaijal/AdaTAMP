# AdaTAMP: Adaptive Task and Motion Planning

**AdaTAMP** is an Adaptive Task and Motion Planning framework that integrates LLM-based task planning with continuous motion planning via a real-time feedback loop, enabling error correction and multi-agent collaboration for embodied agents.

## Abstract

We introduce AdaTAMP, an Adaptive Task and Motion Planning (TAMP) framework leveraging Large Language Models (LLMs) for embodied agents in dynamic environments. AdaTAMP integrates symbolic task planning with continuous motion planning through a real-time self-feedback loop, enabling efficient error correction and seamless multi-agent collaboration. Evaluations conducted in the VirtualHome simulator demonstrate that AdaTAMP significantly outperforms baseline methods in success rate, planning efficiency, and adaptability, particularly for complex, long-horizon, multi-agent scenarios.

## Features

- **LLM-powered Task Planning**: Generates structured action sequences from natural language descriptions
- **Real-time Feedback Loop**: Enables dynamic error correction and plan adaptation
- **Multi-agent Collaboration**: Supports coordinated planning for multiple embodied agents
- **VirtualHome Integration**: Built-in support for household task simulation
- **Schema Validation**: Ensures action sequence integrity with JSON schema validation
- **Comprehensive Evaluation**: Extensive test suite and evaluation framework

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- VirtualHome simulator

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/AdaTAMP.git
   cd AdaTAMP
   ```

2. **Install Python dependencies:**
   ```bash
   pip install openai jsonschema matplotlib tqdm pillow
   ```

3. **Install VirtualHome:**
   Follow the [VirtualHome installation guide](https://github.com/xavierpuigf/virtualhome) to set up the simulator.

4. **Download VirtualHome App:**
   Download the VirtualHome executable and update the `YOUR_FILE_NAME` variable in `evaluate.py` with the path to your VirtualHome app.

5. **Set up OpenAI API:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **⚠️ Security Note:** Never commit your API key to version control. The code is configured to read the API key from environment variables.

6. **Configure VirtualHome path:**
   Update the `YOUR_FILE_NAME` variable in `src/evaluate.py` with the path to your VirtualHome executable:
   ```python
   YOUR_FILE_NAME = "path/to/your/virtualhome/macos_exec.2.2.4.app"
   ```

## Usage

### Basic Task Planning

```python
from src.task_planner import TaskPlanner

# Initialize the task planner
config = MockConfig()  # Use your configuration
planner = TaskPlanner(openai_api_key="your-key", cfg=config)

# Plan a task
task_description = "Make coffee in the kitchen"
action_sequence = planner.plan_task(task_description)
```

### Running Evaluations

```bash
python evaluate.py --task_file resource/test_tasks.json
```

### Running Tests

```bash
python -m pytest src/tests/
```

## Project Structure

```
AdaTAMP/
├── src/
│   ├── task_planner.py      # Main task planning logic
│   ├── vh_environment.py    # VirtualHome environment wrapper
│   ├── vh_utils.py          # Utility functions
│   ├── dict.py              # Object dictionaries (NL ↔ Sim)
│   └── tests/               # Test suite
├── resource/
│   ├── test_tasks.json      # Evaluation tasks
│   ├── task_examples.json   # Example tasks
│   └── *.json               # Object mappings
├── evaluate.py              # Main evaluation script
├── evaluate.ipynb          # Evaluation notebook
└── README.md
```

## Configuration

The framework requires configuration for:

- **Environment Settings**: Observation types, editor mode, base port
- **OpenAI API**: Model selection and API key
- **VirtualHome**: Simulator path and communication settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add your license information here]

## Citation

If you use AdaTAMP in your research, please cite:

```bibtex
@article{adatamp2024,
    title={AdaTAMP: Adaptive Task and Motion Planning for Embodied Agents},
    author={[Authors]},
    journal={[Journal/Conference]},
    year={2024}
}
```