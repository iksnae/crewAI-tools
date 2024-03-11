# Tool Registry

## Overview

The Tool Registry is a component of the CrewAI framework designed for the dynamic registration and retrieval of tools for AI agents. It facilitates modular and scalable development by allowing tools to be easily assigned to agents based on their roles and tasks.

## Features

- **Dynamic Tool Management**: Enables the dynamic registration and retrieval of tools, enhancing the capabilities of agents with flexibility.
- **Simplified Tool Assignment**: Streamlines the development process by allowing registered tools to be seamlessly assigned to agents.
- **Modular Design**: Promotes the development of reusable tools that can be utilized across different agents, improving efficiency and collaboration.
- **JSON Initialization**: Supports initializing the registry with a set of predefined tools from a JSON file, simplifying setup and configuration.

## Getting Started

1. **Installation**: Make sure the CrewAI framework and the dependencies of the Tool Registry are properly installed.
2. **Tool Registration**: Define your tools and register them with the Tool Registry. This can be done programmatically or by loading from a JSON file.
3. **Tool Retrieval**: Retrieve registered tools by name to assign them to agents, enhancing their functionality.

## Example

Define a new tool, register it with the Tool Registry, and demonstrate initialization from a JSON file:

```python
from crewai_tools import Tool
from crewai_tools.tools.tool_registry import ToolRegistry

# Define a new tool
class ExampleTool:
    def run(self, input):
        # Implement tool logic here
        return "Processed " + input

# Initialize the Tool Registry from a JSON file
registry = ToolRegistry(json_file="path/to/initial_tools.json")

# Alternatively, register the ExampleTool manually
registry.register("ExampleTool", ExampleTool)

# Retrieve and use the tool
example_tool_class = registry.get("ExampleTool")
if example_tool_class:
    example_tool = example_tool_class()
    result = example_tool.run("example input")
    print(result)
```

To initialize the registry with predefined tools, create a JSON file (e.g., `initial_tools.json`) with the following structure:

```json
[
  {
    "name": "ExampleTool",
    "tool_class": "ExampleTool"
  }
]
```