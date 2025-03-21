from typing import Any, Dict, Optional

from marble.environments.base_env import BaseEnvironment


class WorldSimulationEnvironment(BaseEnvironment):
    def __init__(
        self, config: Dict[str, Any], name: str = "WorldSimulationEnvironment"
    ):
        """
        Initialize the environment with agents, actions, and conversation tracking.

        Args:
            config (Dict[str, Any]): Configuration including agents and task settings.
        """
        super().__init__(name, config)
        # Register actions
        self.register_action(
            "offer_price",
            handler=self._offer_price_handler,
            description={
                "type": "function",
                "function": {
                    "name": "offer_price",
                    "description": "Make a price offer in the negotiation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "price": {
                                "type": "integer",
                                "description": "The offered price.",
                            },
                            "reason": {
                                "type": "string",
                                "description": "Reason for offering this price.",
                                "optional": True,
                            },
                        },
                        "required": ["price"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        self.register_action(
            "accept_offer",
            handler=self._accept_offer_handler,
            description={
                "type": "function",
                "function": {
                    "name": "accept_offer",
                    "description": "Accept the current offer to finalize the negotiation.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
        )

        self.register_action(
            "reject_and_counter",
            handler=self._reject_and_counter_handler,
            description={
                "type": "function",
                "function": {
                    "name": "reject_and_counter",
                    "description": "Reject the current offer and provide a counter offer.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "counter_price": {
                                "type": "integer",
                                "description": "The counter offer price.",
                            },
                            "reason": {
                                "type": "string",
                                "description": "Reason for the counter offer.",
                                "optional": True,
                            },
                        },
                        "required": ["counter_price"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        self.register_action(
            "provide_information",
            handler=self._provide_information_handler,
            description={
                "type": "function",
                "function": {
                    "name": "provide_information",
                    "description": "Provide supporting information to justify the price or other negotiation details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "info_type": {
                                "type": "string",
                                "description": "Type of information (e.g., Vehicle History, Market Comparison).",
                            },
                            "details": {
                                "type": "string",
                                "description": "Detailed information or justification.",
                            },
                        },
                        "required": ["info_type", "details"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        self.register_action(
            "inquire_intentions",
            handler=self._inquire_intentions_handler,
            description={
                "type": "function",
                "function": {
                    "name": "inquire_intentions",
                    "description": "Ask the other party about their intentions or expectations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question to ask the other party.",
                            }
                        },
                        "required": ["question"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        self.register_action(
            "end_negotiation",
            handler=self._end_negotiation_handler,
            description={
                "type": "function",
                "function": {
                    "name": "end_negotiation",
                    "description": "End the negotiation without an agreement.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
        )

    # Handler implementations
    def _offer_price_handler(
        self, price: int, reason: Optional[str] = None
    ) -> Dict[str, Any]:
        # Logic for offering a price
        response = {
            "success": True,
            "offered_price": price,
            "reason": reason or "No reason provided",
        }
        # print("*********************action handler _offer_price_handler*********************") # debug info
        print(f"Offer Price: {price}, Reason: {reason}")
        return response

    def _accept_offer_handler(self) -> Dict[str, Any]:
        # Logic for accepting an offer
        # print("*********************action handler _accept_offer_handler*********************") # debug info
        response = {
            "success": True,
            "message": "Offer accepted. Negotiation concluded.",
        }
        print("Accept Offer")
        self.done = True
        return response

    def _reject_and_counter_handler(
        self, counter_price: int, reason: Optional[str] = None
    ) -> Dict[str, Any]:
        # Logic for rejecting an offer and countering with a new price
        # print("*********************action handler _reject_and_counter_handler*********************") # debug info
        response = {
            "success": True,
            "counter_price": counter_price,
            "reason": reason or "No reason provided",
        }
        print(f"Reject and Counter Offer: {counter_price}, Reason: {reason}")
        return response

    def _provide_information_handler(
        self, info_type: str, details: str
    ) -> Dict[str, Any]:
        # Logic for providing information
        # print("*********************action handler _provide_information_handler*********************") # debug info
        response = {"success": True, "info_type": info_type, "details": details}
        print(f"Provide Information: {info_type}, Details: {details}")
        return response

    def _inquire_intentions_handler(self, question: str) -> Dict[str, Any]:
        # Logic for inquiring intentions
        # print("*********************action handler _inquire_intentions_handler*********************") # debug info
        response = {
            "success": True,
            "question": question,
            "response": "Response from the other party.",
        }
        print(f"Inquire Intentions: {question}")
        return response

    def _end_negotiation_handler(self) -> Dict[str, Any]:
        # Logic for ending the negotiation without an agreement
        # print("*********************action handler _end_negotiation_handler*********************") # debug info
        response = {"success": True, "message": "Negotiation ended without agreement."}
        print("End Negotiation")
        self.done = True
        return response
