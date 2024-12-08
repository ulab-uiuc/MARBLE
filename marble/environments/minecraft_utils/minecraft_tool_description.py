scanNearbyEntities_description = {
    "type": "function",
    "function": {
        "name": "scanNearbyEntities",
        "description": "Find minecraft item blocks creatures in a radius.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The center of the area to be scanned.",
                },
                "radius": {
                    "type": "number",
                    "description": "The radius of the area to be scanned.",
                },
                "item_num": {
                    "type": "number",
                    "description": "The number of items you want to find.",
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

navigateTo_description = {
    "type": "function",
    "function": {
        "name": "navigateTo",
        "description": "Move to a specific position x y z.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "number",
                    "description": "The x coordinate.",
                },
                "y": {
                    "type": "number",
                    "description": "The y coordinate.",
                },
                "z": {
                    "type": "number",
                    "description": "The z coordinate.",
                }
            },
            "required": ["x", "y", "z"],
            "additionalProperties": False
        }
    }
}

attackTarget_description = {
    "type": "function",
    "function": {
        "name": "attackTarget",
        "description": "Attack the nearest entity with a specific name.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_name": {
                    "type": "string",
                    "description": "The name of the entity to attack.",
                }
            },
            "required": ["target_name"],
            "additionalProperties": False
        }
    }
}

navigateToBuilding_description = {
    "type": "function",
    "function": {
        "name": "navigateToBuilding",
        "description": "Move to a building by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "building_name": {
                    "type": "string",
                    "description": "The name of the building to move to.",
                }
            },
            "required": ["building_name"],
            "additionalProperties": False
        }
    }
}

navigateToAnimal_description = {
    "type": "function",
    "function": {
        "name": "navigateToAnimal",
        "description": "Move to an animal by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "animal_name": {
                    "type": "string",
                    "description": "The name of the animal to move to.",
                }
            },
            "required": ["animal_name"],
            "additionalProperties": False
        }
    }
}

navigateToPlayer_description = {
    "type": "function",
    "function": {
        "name": "navigateToPlayer",
        "description": "Move to a target player.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_name": {
                    "type": "string",
                    "description": "The name of the player to move to.",
                }
            },
            "required": ["target_name"],
            "additionalProperties": False
        }
    }
}

UseItemOnEntity_description = {
    "type": "function",
    "function": {
        "name": "UseItemOnEntity",
        "description": "Use a specific item on a specific entity.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be used.",
                },
                "entity_name": {
                    "type": "string",
                    "description": "The name of the entity to apply the item to.",
                }
            },
            "required": ["item_name", "entity_name"],
            "additionalProperties": False
        }
    }
}

sleep_description = {
    "type": "function",
    "function": {
        "name": "sleep",
        "description": "Go to sleep.",
    }
}

wake_description = {
    "type": "function",
    "function": {
        "name": "wake",
        "description": "Wake up.",
    }
}

MineBlock_description = {
    "type": "function",
    "function": {
        "name": "MineBlock",
        "description": "Dig block at specific position x y z.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "number",
                    "description": "The x coordinate.",
                },
                "y": {
                    "type": "number",
                    "description": "The y coordinate.",
                },
                "z": {
                    "type": "number",
                    "description": "The z coordinate.",
                }
            },
            "required": ["x", "y", "z"],
            "additionalProperties": False
        }
    }
}

placeBlock_description = {
    "type": "function",
    "function": {
        "name": "placeBlock",
        "description": "Place a specific item at specific position x y z with specific facing in one of [W, E, S, N, x, y, z, A] default is 'A'.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to place.",
                },
                "x": {
                    "type": "number",
                    "description": "The x coordinate of the item position.",
                },
                "y": {
                    "type": "number",
                    "description": "The y coordinate of the item position.",
                },
                "z": {
                    "type": "number",
                    "description": "The z coordinate of the item position.",
                },
                "facing": {
                    "type": "string",
                    "description": "The facing direction of the item after it is placed.",
                }
            },
            "required": ["item_name", "x", "y", "z", "facing"],
            "additionalProperties": False
        }
    }
}

equipItem_description = {
    "type": "function",
    "function": {
        "name": "equipItem",
        "description": "Equip a specific item on a specific slot or to equip item on hand,head,torso,legs,feet,off-hand.",
        "parameters": {
            "type": "object",
            "properties": {
                "slot": {
                    "type": "string",
                    "description": "The name of the slot to equip the item on.",
                },
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be equipped.",
                }
            },
            "required": ["slot", "item_name"],
            "additionalProperties": False
        }
    }
}

tossItem_description = {
    "type": "function",
    "function": {
        "name": "tossItem",
        "description": "Throw a specific item out with a specific count.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be throwed.",
                },
                "count": {
                    "type": "number",
                    "description": "The count of the item to be throwed.",
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

talkTo_description = {
    "type": "function",
    "function": {
        "name": "talkTo",
        "description": "Talk to the entity.",
        "parameters": {
            "type": "object",
            "properties": {
                "entity_name": {
                    "type": "string",
                    "description": "The name of the entity to talk to.",
                },
                "message": {
                    "type": "string",
                    "description": "The message to be conveyed.",
                }
            },
            "required": ["entity_name", "message"],
            "additionalProperties": False
        }
    }
}

handoverBlock_description = {
    "type": "function",
    "function": {
        "name": "handoverBlock",
        "description": "Hand item to a target player you work with.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_player_name": {
                    "type": "string",
                    "description": "The name of the player you want to hand the item to.",
                },
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be passed.",
                },
                "item_count": {
                    "type": "number",
                    "description": "The count of the item to be passed.",
                }
            },
            "required": ["target_player_name", "item_name", "item_count"],
            "additionalProperties": False
        }
    }
}

withdrawItem_description = {
    "type": "function",
    "function": {
        "name": "withdrawItem",
        "description": "Take out item from nearest 'chest' | 'container' | 'furnace'.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be taken out.",
                },
                "from_name": {
                    "type": "string",
                    "description": "Where the item will be taken out from.",
                },
                "item_count": {
                    "type": "number",
                    "description": "The count of the item to be taken out.",
                }
            },
            "required": ["item_name", "from_name", "item_count"],
            "additionalProperties": False
        }
    }
}

storeItem_description = {
    "type": "function",
    "function": {
        "name": "storeItem",
        "description": "Put in item to one chest, container, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be stored.",
                },
                "to_name": {
                    "type": "string",
                    "description": "Where the item will be stored.",
                },
                "item_count": {
                    "type": "number",
                    "description": "The count of the item to be stored.",
                }
            },
            "required": ["item_name", "to_name", "item_count"],
            "additionalProperties": False
        }
    }
}

craftBlock_description = {
    "type": "function",
    "function": {
        "name": "craftBlock",
        "description": "Craft item in the crafting table.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to craft.",
                },
                "count": {
                    "type": "number",
                    "description": "The count of the item to craft.",
                }
            },
            "required": ["item_name", "count"],
            "additionalProperties": False
        }
    }
}

SmeltingCooking_description = {
    "type": "function",
    "function": {
        "name": "SmeltingCooking",
        "description": "Smelt or cook item in the furnace.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to cook or smelt.",
                },
                "item_count": {
                    "type": "number",
                    "description": "The count of the item to cook or smelt.",
                },
                "fuel_item_name": {
                    "type": "string",
                    "description": "The name of the item to use as fuel.",
                }
            },
            "required": ["item_name", "item_count", "fuel_item_name"],
            "additionalProperties": False
        }
    }
}

erectDirtLadder_description = {
    "type": "function",
    "function": {
        "name": "erectDirtLadder",
        "description": "Helpful to place item at higher place. Erect a dirt ladder structure at specific position x y z. Remember to dismantle it after use.",
        "parameters": {
            "type": "object",
            "properties": {
                "top_x": {
                    "type": "number",
                    "description": "The x coordinate of the top of the ladder.",
                },
                "top_y": {
                    "type": "number",
                    "description": "The y coordinate of the top of the ladder.",
                },
                "top_z": {
                    "type": "number",
                    "description": "The z coordinate of the top of the ladder.",
                }
            },
            "required": ["top_x", "top_y", "top_z"],
            "additionalProperties": False
        }
    }
}

dismantleDirtLadder_description = {
    "type": "function",
    "function": {
        "name": "dismantleDirtLadder",
        "description": "Dismantle a dirt ladder structure from ground to top at specific position x y z.",
        "parameters": {
            "type": "object",
            "properties": {
                "top_x": {
                    "type": "number",
                    "description": "The x coordinate of the top of the ladder.",
                },
                "top_y": {
                    "type": "number",
                    "description": "The y coordinate of the top of the ladder.",
                },
                "top_z": {
                    "type": "number",
                    "description": "The z coordinate of the top of the ladder.",
                }
            },
            "required": ["top_x", "top_y", "top_z"],
            "additionalProperties": False
        }
    }
}

enchantItem_description = {
    "type": "function",
    "function": {
        "name": "enchantItem",
        "description": "Enchant item in the enchanting table.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be enchanted.",
                },
                "count": {
                    "type": "number",
                    "description": "The count of the item to be enchanted.",
                }
            },
            "required": ["item_name", "count"],
            "additionalProperties": False
        }
    }
}

trade_description = {
    "type": "function",
    "function": {
        "name": "trade",
        "description": "Trade item with the villager npc.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be traded.",
                },
                "with_name": {
                    "type": "string",
                    "description": "The name of the village npc to trade with.",
                },
                "count": {
                    "type": "number",
                    "description": "The count of the item to be traded.",
                }
            },
            "required": ["item_name", "with_name", "count"],
            "additionalProperties": False
        }
    }
}

repairItem_description = {
    "type": "function",
    "function": {
        "name": "repairItem",
        "description": "Repair item in the anvil.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to be repaired.",
                },
                "material": {
                    "type": "string",
                    "description": "The material to be used for reparation.",
                }
            },
            "required": ["item_name", "material"],
            "additionalProperties": False
        }
    }
}

eat_description = {
    "type": "function",
    "function": {
        "name": "eat",
        "description": "Eat item.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to eat.",
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

drink_description = {
    "type": "function",
    "function": {
        "name": "drink",
        "description": "Drink item.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to drink.",
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

wear_description = {
    "type": "function",
    "function": {
        "name": "wear",
        "description": "Wear item on specific slot.",
        "parameters": {
            "type": "object",
            "properties": {
                "slot": {
                    "type": "string",
                    "description": "The name of the slot to wear the item on.",
                },
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to wear.",
                }
            },
            "required": ["slot", "item_name"],
            "additionalProperties": False
        }
    }
}

layDirtBeam_description = {
    "type": "function",
    "function": {
        "name": "layDirtBeam",
        "description": "Lay a dirt beam from position x1 y1 z1 to position x2 y2 z2.",
        "parameters": {
            "type": "object",
            "properties": {
                "x_1": {
                    "type": "number",
                    "description": "The starting x coordinate of the dirt beam to lay.",
                },
                "y_1": {
                    "type": "number",
                    "description": "The starting y coordinate of the dirt beam to lay.",
                },
                "z_1": {
                    "type": "number",
                    "description": "The starting z coordinate of the dirt beam to lay.",
                },
                "x_2": {
                    "type": "number",
                    "description": "The ending x coordinate of the dirt beam to lay.",
                },
                "y_2": {
                    "type": "number",
                    "description": "The ending y coordinate of the dirt beam to lay.",
                },
                "z_2": {
                    "type": "number",
                    "description": "The ending z coordinate of the dirt beam to lay.",
                }
            },
            "required": ["x_1", "y_1", "z_1", "x_2", "y_2", "z_2"],
            "additionalProperties": False
        }
    }
}

removeDirtBeam_description = {
    "type": "function",
    "function": {
        "name": "removeDirtBeam",
        "description": "Remove a dirt beam from position x1 y1 z1 to position x2 y2 z2.",
        "parameters": {
            "type": "object",
            "properties": {
                "x_1": {
                    "type": "number",
                    "description": "The starting x coordinate of the dirt beam to remove.",
                },
                "y_1": {
                    "type": "number",
                    "description": "The starting y coordinate of the dirt beam to remove.",
                },
                "z_1": {
                    "type": "number",
                    "description": "The starting z coordinate of the dirt beam to remove.",
                },
                "x_2": {
                    "type": "number",
                    "description": "The ending x coordinate of the dirt beam to remove.",
                },
                "y_2": {
                    "type": "number",
                    "description": "The ending y coordinate of the dirt beam to remove.",
                },
                "z_2": {
                    "type": "number",
                    "description": "The ending z coordinate of the dirt beam to remove.",
                }
            },
            "required": ["x_1", "y_1", "z_1", "x_2", "y_2", "z_2"],
            "additionalProperties": False
        }
    }
}

openContainer_description = {
    "type": "function",
    "function": {
        "name": "openContainer",
        "description": "Open the nearest 'chest' | 'container' | 'furnace'. Position x y z is optional.",
        "parameters": {
            "type": "object",
            "properties": {
                "container_name": {
                    "type": "string",
                    "description": "The name of the container to open.",
                },
                "position": {
                    "type": "array",
                    "description": "The position of the container to open.",
                    "items": {
                        "type": "number"
                    }
                }
            },
            "required": ["container_name"],
            "additionalProperties": False
        }
    }
}

closeContainer_description = {
    "type": "function",
    "function": {
        "name": "closeContainer",
        "description": "Close the nearest 'chest' | 'container' | 'furnace'. Position x y z is optional.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the container to close.",
                },
                "position": {
                    "type": "array",
                    "description": "The position of the container to close.",
                    "items": {
                        "type": "number"
                    }
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

fetchContainerContents_description = {
    "type": "function",
    "function": {
        "name": "fetchContainerContents",
        "description": "Get the details of the 'chest' | 'container' | 'furnace'. Position x y z is optional.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the container to fetch content of.",
                },
                "position": {
                    "type": "array",
                    "description": "The position of the container to fetch content of.",
                    "items": {
                        "type": "number"
                    }
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

toggleAction_description = {
    "type": "function",
    "function": {
        "name": "toggleAction",
        "description": "Open/Close gate, lever, or press button (pressure_plate need to stand on it, iron door need to be powered, they are not included), at specific position x y z.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to toggle.",
                },
                "x": {
                    "type": "number",
                    "description": "The x coordinate of the item to toggle.",
                },
                "y": {
                    "type": "number",
                    "description": "The y coordinate of the item to toggle.",
                },
                "z": {
                    "type": "number",
                    "description": "The z coordinate of the item to toggle.",
                }
            },
            "required": ["item_name", "x", "y", "z"],
            "additionalProperties": False
        }
    }
}

get_entity_info_description = {
    "type": "function",
    "function": {
        "name": "get_entity_info",
        "description": "Get the entity information.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_name": {
                    "type": "string",
                    "description": "The name of the target item.",
                }
            },
            "required": ["target_name"],
            "additionalProperties": False
        }
    }
}

get_environment_info_description = {
    "type": "function",
    "function": {
        "name": "get_environment_info",
        "description": "Get the environment information.",
    }
}

performMovement_description = {
    "type": "function",
    "function": {
        "name": "performMovement",
        "description": "Perform action (jump/forward/back/left/right) for seconds.",
        "parameters": {
            "type": "object",
            "properties": {
                "action_name": {
                    "type": "string",
                    "description": "The name of the target action.",
                },
                "seconds": {
                    "type": "number",
                    "description": "How many seconds the action lasts for.",
                }
            },
            "required": ["action_name", "seconds"],
            "additionalProperties": False
        }
    }
}

lookAt_description = {
    "type": "function",
    "function": {
        "name": "lookAt",
        "description": "Look at someone or something.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the target to look at.",
                }
            },
            "required": ["name"],
            "additionalProperties": False
        }
    }
}

startFishing_description = {
    "type": "function",
    "function": {
        "name": "startFishing",
        "description": "Start fishing.",
    }
}

stopFishing_description = {
    "type": "function",
    "function": {
        "name": "stopFishing",
        "description": "Stop fishing.",
    }
}

read_description = {
    "type": "function",
    "function": {
        "name": "read",
        "description": "Read book or sign neaby.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the book or sgin to read.",
                }
            },
            "required": ["item_name"],
            "additionalProperties": False
        }
    }
}

readPage_description = {
    "type": "function",
    "function": {
        "name": "readPage",
        "description": "Read content from book page.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the book to read.",
                },
                "page": {
                    "type": "number",
                    "description": "The page number of the book to read.",
                }
            },
            "required": ["item_name", "page"],
            "additionalProperties": False
        }
    }
}

write_description = {
    "type": "function",
    "function": {
        "name": "write",
        "description": "Write content on writable book or sign.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "The name of the book or sign to write on.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write on the book or sign.",
                }
            },
            "required": ["item_name", "content"],
            "additionalProperties": False
        }
    }
}