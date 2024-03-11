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

    def __init__(self):
        """Initializes the ToolRegistry with an empty registry."""
        self._registry: Dict[str, Type[Tool]] = {}

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
