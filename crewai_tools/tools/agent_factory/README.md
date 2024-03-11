For a complete and detailed README including an example for the Agent Factory, follow the structure below, adding a practical example section as requested:

# Agent Factory

## Overview

The Agent Factory dynamically creates and manages Agent instances in the CrewAI framework using JSON-based configurations, enhancing deployment flexibility and scalability.

## Features

- **Dynamic Agent Creation**: Instantiates agents from JSON configurations.
- **Tool Assignment**: Dynamically assigns tools to agents through the ToolRegistry.
- **Extensibility**: Easily extended for various use cases.

## Getting Started

1. **Installation**: Ensure CrewAI framework and dependencies are installed.
2. **Configuration**: Define agents and tools in a JSON configuration.
3. **Initialization**: Instantiate AgentFactory with your JSON configuration path.
4. **Usage**: Create agents or retrieve all configured agents.

## Example

```json
// agents.json
{
  "agents": [
    {
      "role": "Example Agent",
      "goal": "Demonstrate Agent Factory usage",
      "backstory": "Created for demonstration purposes",
      "verbose": true,
      "tools": [
        {
          "type": "ExampleTool",
          "name": "ExampleToolName",
          "description": "An example tool",
          "config": {}
        }
      ]
    }
  ]
}
```

```python
from agent_factory import AgentFactory

# Initialize AgentFactory with path to JSON configuration
factory = AgentFactory("path/to/agents.json")

# Create and retrieve all agents
agents = factory.get_all_agents()
```
