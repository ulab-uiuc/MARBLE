"""
Operation registry module for managing operation nodes.
"""

from typing import Dict, Type

from marble.swarm.node import Node


class OperationRegistry:
    registry: Dict[str, Type[Node]] = {}

    @classmethod
    def register(cls, name: str, node_class: Type[Node]):
        cls.registry[name] = node_class

    @classmethod
    def get(cls, name: str) -> Type[Node]:
        return cls.registry.get(name)

    @classmethod
    def keys(cls):
        return cls.registry.keys()
