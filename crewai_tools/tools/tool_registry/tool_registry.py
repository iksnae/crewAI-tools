import json
from typing import Type, Dict, List, Optional
from crewai_tools import Tool

class ToolRegistry:
    """
    A registry for managing tool classes in the CrewAI framework. 
    Allows for the dynamic registration and retrieval of tool classes by name.

    Attributes:
        _registry (Dict[str, Type[Tool]]): A private dictionary that stores tool classes keyed by their names.

    Methods:
        register(name, tool_class): Registers a tool class with a specific name.
        get(name): Retrieves a tool class by its name, returning None if not found.
        list_tools(): Returns a list of all registered tool names.
    """

    def __init__(self, json_file: Optional[str] = None):
        """
        Initializes the ToolRegistry. Optionally loads initial tool definitions from a JSON file.

        Parameters:
            json_file (Optional[str]): The path to a JSON file containing tool definitions.
                The JSON file should be an array of objects, each with a "name" and "tool_class" field.
        """
        self._registry: Dict[str, Type[Tool]] = {}
        if json_file:
            self._load_tools_from_json(json_file)

    def _load_tools_from_json(self, file_path: str) -> None:
        """
        Loads tool definitions from a JSON file and registers them.

        Parameters:
            file_path (str): The path to the JSON file containing tool definitions.
        """
        try:
            with open(file_path, 'r') as file:
                tools = json.load(file)
                for tool in tools:
                    # Assuming the tool_class is a string that matches a class name in the scope
                    # This requires further logic to safely turn string into class reference
                    tool_class = globals().get(tool['tool_class'])
                    if tool_class and issubclass(tool_class, Tool):
                        self.register(tool['name'], tool_class)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Failed to load tool definitions from {file_path}: {e}")


    def register(self, name: str, tool_class: Type[Tool]) -> None:
        """
        Registers a tool class with a specific name.

        Parameters:
            name (str): The name to register the tool class under.
            tool_class (Type[Tool]): The tool class to be registered.
        """
        self._registry[name] = tool_class

    def get(self, name: str) -> Optional[Type[Tool]]:
        """
        Retrieves a tool class by its name.

        Parameters:
            name (str): The name of the tool class to retrieve.

        Returns:
            Optional[Type[Tool]]: The tool class if found, otherwise None.
        """
        return self._registry.get(name)

    def list_tools(self) -> List[str]:
        """
        Lists all registered tool names.

        Returns:
            List[str]: A list of the names of all registered tools.
        """
        return list(self._registry.keys())
