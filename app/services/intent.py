from typing import Dict, List
import re

class IntentService:
    def __init__(self):
        self.intent_patterns = {
            "menu_inquiry": [
                r"menu",
                r"what.*serve",
                r"what.*have",
                r"what.*offer",
                r"what.*available",
                r"what.*special",
                r"what.*dish",
                r"what.*food",
                r"vegetarian",
                r"vegan",
                r"gluten-free",
                r"price",
                r"cost",
                r"how much",
                r"dietary",
                r"allergy"
            ],
            "reservation_request": [
                r"reservation",
                r"book",
                r"table",
                r"reserve",
                r"booking",
                r"when.*available",
                r"what.*time.*available",
                r"party.*size",
                r"how many.*people",
                r"special.*request",
                r"dietary.*requirement"
            ],
            "hours_location": [
                r"hour",
                r"open",
                r"close",
                r"when.*open",
                r"when.*close",
                r"where.*located",
                r"address",
                r"location",
                r"directions",
                r"how.*get.*there",
                r"parking",
                r"transportation"
            ],
            "special_events": [
                r"event",
                r"special",
                r"promotion",
                r"discount",
                r"offer",
                r"deal",
                r"happy hour",
                r"live music",
                r"entertainment"
            ],
            "general_inquiry": [
                r"hi",
                r"hello",
                r"hey",
                r"help",
                r"what.*can.*do",
                r"how.*can.*help",
                r"tell.*me.*about",
                r"who.*are.*you",
                r"what.*are.*you"
            ]
        }

    async def detect_intent(self, message: str) -> str:
        message = message.lower()
        max_matches = 0
        detected_intent = "general_inquiry"

        for intent, patterns in self.intent_patterns.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, message))
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent

        return detected_intent

    def get_intent_confidence(self, message: str) -> Dict[str, float]:
        message = message.lower()
        confidence_scores = {}

        for intent, patterns in self.intent_patterns.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, message))
            total_patterns = len(patterns)
            confidence = matches / total_patterns if total_patterns > 0 else 0
            confidence_scores[intent] = confidence

        return confidence_scores 