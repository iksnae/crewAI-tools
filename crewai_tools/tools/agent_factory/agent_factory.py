import json
from typing import Dict, List, Any
from crewai import Agent
from crewai_tools import Tool
from crewai_tools.tools.tool_registry import ToolRegistry

class AgentFactory:
    """
    Facilitates the creation of Agent instances from definitions stored in a JSON file,
    using a ToolRegistry for dynamic tool assignment.

    Attributes:
        tool_registry (ToolRegistry): Manages tool assignments.
        json_path (str): Path to the JSON file with agent definitions.
        agents_data (List[Dict[str, Any]]): Loaded agent definitions from JSON.

    Methods:
        load_agents_data() -> List[Dict[str, Any]]:
            Loads and parses agent definitions from the JSON file.

        create_agent(agent_info: Dict[str, Any]) -> Agent:
            Creates an Agent instance from the provided definition, assigning tools as defined.

        get_all_agents() -> List[Agent]:
            Returns a list of all agents defined in the JSON file, instantiated with their respective tools.
    """
    def __init__(self, json_path: str):
        self.tool_registry: ToolRegistry = ToolRegistry()
        self.json_path: str = json_path
        self.agents_data: List[Dict[str, Any]] = self.load_agents_data()

    def load_agents_data(self) -> List[Dict[str, Any]]:
        """Loads and parses agent definitions from JSON."""
        with open(self.json_path, 'r') as file:
            data = json.load(file)
        return data.get('agents', [])

    def create_agent(self, agent_info: Dict[str, Any]) -> Agent:
        """Creates an Agent with the specified attributes and tools."""
        agent = Agent(
            role=agent_info['role'],
            goal=agent_info['goal'],
            backstory=agent_info['backstory'],
            verbose=agent_info.get('verbose', False)
        )
        if "tools" in agent_info:
            for tool_info in agent_info["tools"]:
                tool_class = self.tool_registry.get(tool_info["type"])
                if tool_class:
                    tool_instance = tool_class(**tool_info["config"])
                    agent.assign_tool(Tool(name=tool_info["name"], func=tool_instance.run, description=tool_info["description"]))
        return agent

    def get_all_agents(self) -> List[Agent]:
        """Returns a list of all instantiated agents."""
        return [self.create_agent(agent_info) for agent_info in self.agents_data]
