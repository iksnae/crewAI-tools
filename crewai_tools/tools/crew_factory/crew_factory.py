import json
from typing import Dict, List, Any
from crewai import Crew, Process, Task
from pydantic import TypeAdapter
from ..agent_factory.agent_factory import AgentFactory

class CrewFactory:
    """
    Factory class for creating Crew objects from a JSON configuration.

    Attributes:
        json_path (str): Path to the JSON file containing the crew configurations.
        agent_factory (AgentFactory): An instance of the AgentFactory to create agents for the crews.
        crews_data (List[Dict[str, Any]]): Loaded crew configurations from the JSON file.
    """
    def __init__(self, json_path: str, agent_factory: AgentFactory):
        self.json_path = json_path
        self.agent_factory = agent_factory
        self.crews_data = self.load_crews_data()

    def load_crews_data(self) -> List[Dict[str, Any]]:
        """Loads and returns the crew configurations from the JSON file."""
        with open(self.json_path, 'r') as file:
            data = json.load(file)
        return data.get('crews', [])

    def create_crew(self, crew_info: Dict[str, Any]) -> Crew:
        """
        Creates a Crew object from the provided configuration.

        Args:
            crew_info (Dict[str, Any]): The dictionary containing the configuration for the crew.

        Returns:
            Crew: An instantiated Crew object based on the provided configuration.
        """
        # Assign agents to tasks
        for task_info in crew_info.get("tasks", []):
            agent_role = task_info.pop("agent", None)
            if agent_role:
                agent = self.agent_factory.get_agent_by_role(agent_role)
                if agent:
                    task_info["agent"] = agent
                else:
                    print(f"Agent with role {agent_role} not found.")
        crew_info["tasks"] = [Task(**task_info) for task_info in crew_info.get("tasks", [])]

        # Use TypeAdapter for Crew instantiation
        try:
            crew_adapter = TypeAdapter(Crew)
            crew = crew_adapter.validate_python(crew_info)
            return crew
        except Exception as e:
            print(f"Error creating crew: {e}")
            return None

    def get_all_crews(self) -> List[Crew]:
        """Returns a list of all Crew objects instantiated from the JSON configuration."""
        return [self.create_crew(crew_info) for crew_info in self.crews_data if self.create_crew(crew_info)]

    def get_crew_by_name(self, name: str) -> Crew:
        """
        Fetches and instantiates a specific crew by its name from the loaded configurations.

        Args:
            name (str): The name of the crew to fetch.

        Returns:
            Crew: The instantiated Crew object, if found; otherwise, None.
        """
        for crew_info in self.crews_data:
            if crew_info['name'] == name:
                return self.create_crew(crew_info)
        return None
    

if __name__ == "__main__":
    # Example usage of the CrewFactory
    json_path = "./agency.json"  # Update with the actual path to your JSON file
    agent_factory = AgentFactory(...)  # Initialize your AgentFactory here
    crew_factory = CrewFactory(json_path, agent_factory)

    # Fetch and print details of a specific crew
    crew_name = "Content Creation Crew"
    crew = crew_factory.get_crew_by_name(crew_name)
    if crew:
        print(f"Crew Name: {crew.name}")
        for task in crew.tasks:
            print(f"Task: {task.description}, Assigned to: {task.agent.role}")
    else:
        print(f"No crew found with the name: {crew_name}")