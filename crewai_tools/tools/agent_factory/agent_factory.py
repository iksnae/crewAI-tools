import json
from typing import Dict, List, Any, Optional
from crewai import Agent
from crewai_tools.tools.base_tool import Tool
from crewai_tools.tools.tool_registry.tool_registry import ToolRegistry
from langchain_community.llms.ollama import Ollama
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
    def __init__(self, json_path: str, tool_registry = ToolRegistry()):
        self.tool_registry: ToolRegistry = tool_registry
        self.json_path: str = json_path
        self.agents_data: List[Dict[str, Any]] = self.load_agents_data()
        print(f'Registered {len(self.agents_data)} Agents')

    def load_agents_data(self) -> List[Dict[str, Any]]:
        """Loads and parses agent definitions from JSON."""
        with open(self.json_path, 'r') as file:
            data = json.load(file)
        return data.get('agents', [])

    def create_agent(self, agent_info: Dict[str, Any]) -> Agent:
        """Creates an Agent with the specified attributes and tools."""
        basic_attrs = {k: v for k, v in agent_info.items() if k in ["role", "goal", "backstory", "max_iter", "max_rpm", "verbose", "allow_delegation"]}
        agent = Agent(**basic_attrs)

        if "model_name" in agent_info:
            agent.llm = Ollama(model=agent_info["model_name"])
    
        if "memory" in agent_info:
            agent.memory = agent_info["memory"]

        if "tools" in agent_info:
            for tool_info in agent_info["tools"]:
                tool_class = self.tool_registry.get(tool_info["type"])
                if tool_class:
                    tool_instance = tool_class(**tool_info["config"])
                    agent.tools.append(tool_instance)
                else:
                    print(f'no tool class found for {tool_class}')
        return agent

    def get_all_agents(self) -> List[Agent]:
        """Returns a list of all instantiated agents."""
        return [self.create_agent(agent_info) for agent_info in self.agents_data]

    def get_agent_by_role(self, role: str) -> Optional[Agent]:
        """
        Fetches a specific agent by its role.

        Args:
            role (str): The role of the agent to fetch.

        Returns:
            Optional[Agent]: An instantiated Agent object if found, otherwise None.
        """
        for agent_info in self.agents_data:
            if agent_info['role'] == role:
                return self.create_agent(agent_info)
        return None