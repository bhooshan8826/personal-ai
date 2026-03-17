"""
Intent parsing and entity extraction
"""
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import re
from core.llm_engine import get_llm_engine

logger = logging.getLogger(__name__)


class IntentParser:
    """Parse user intent and extract entities"""

    INTENT_KEYWORDS = {
        "task_creation": ["create task", "add task", "remind me to", "i need to", "todo", "schedule"],
        "task_update": ["update task", "edit task", "change task", "modify task"],
        "task_completion": ["mark as done", "complete task", "finished", "done with"],
        "task_deletion": ["delete task", "remove task", "cancel task"],
        "task_list": ["list tasks", "show tasks", "my tasks", "what tasks"],
        "note_creation": ["create note", "add note", "save note", "write note"],
        "note_search": ["find note", "search note", "find notes", "search notes"],
        "reminder_creation": ["set reminder", "remind me", "alert me"],
        "email_draft": ["draft email", "compose email", "write email"],
        "knowledge_search": ["search", "find", "look up", "what is"],
        "general_question": ["hello", "hi", "how", "what", "why", "tell me"],
    }

    def __init__(self):
        """Initialize intent parser"""
        self.llm = get_llm_engine()

    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse user input and extract intent and entities
        Returns: {intent, entities, confidence}
        """
        text_lower = text.lower().strip()

        # First, try fast keyword matching
        intent_result = self._fast_keyword_match(text_lower)
        if intent_result and intent_result.get("confidence", 0) > 0.8:
            return intent_result

        # Fall back to LLM-based classification
        try:
            return self.llm.classify_intent(text)
        except Exception as e:
            logger.error(f"Error in LLM intent classification: {e}")
            return {
                "intent": "general_question",
                "entities": {},
                "confidence": 0.3,
            }

    def _fast_keyword_match(self, text: str) -> Dict[str, Any]:
        """Quick keyword-based intent matching"""
        scores = {}

        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[intent] = score

        if not scores:
            return None

        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 3, 1.0)  # Normalize confidence

        entities = self._extract_entities_fast(text, best_intent)

        return {
            "intent": best_intent,
            "entities": entities,
            "confidence": confidence,
        }

    def _extract_entities_fast(self, text: str, intent: str) -> Dict[str, Any]:
        """Fast entity extraction using regex patterns"""
        entities = {}

        # Extract priority
        if re.search(r"\b(high|urgent|critical)\b", text):
            entities["priority"] = "high"
        elif re.search(r"\b(low|whenever)\b", text):
            entities["priority"] = "low"
        else:
            entities["priority"] = "medium"

        # Extract time expressions
        time_entity = self._extract_time(text)
        if time_entity:
            entities["deadline"] = time_entity

        # Extract quoted text (task description or note content)
        quoted = re.findall(r'"([^"]+)"', text)
        if quoted:
            entities["content"] = quoted[0]

        # Extract email patterns
        email = re.search(r"[\w\.-]+@[\w\.-]+", text)
        if email:
            entities["email"] = email.group()

        return entities

    def _extract_time(self, text: str) -> str:
        """Extract time references from text"""
        now = datetime.now()

        # Tomorrow
        if "tomorrow" in text:
            tomorrow = now + timedelta(days=1)
            return tomorrow.strftime("%Y-%m-%d")

        # Today
        if "today" in text:
            return now.strftime("%Y-%m-%d")

        # Days of week
        days_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        for day_name, day_num in days_map.items():
            if day_name in text:
                # Find next occurrence of this day
                current_day = now.weekday()
                days_ahead = day_num - current_day
                if days_ahead <= 0:
                    days_ahead += 7
                future_date = now + timedelta(days=days_ahead)
                return future_date.strftime("%Y-%m-%d")

        # Numbers like "in 3 days"
        match = re.search(r"in (\d+) days?", text)
        if match:
            days = int(match.group(1))
            future_date = now + timedelta(days=days)
            return future_date.strftime("%Y-%m-%d")

        # "Next week"
        if "next week" in text:
            future_date = now + timedelta(weeks=1)
            return future_date.strftime("%Y-%m-%d")

        # Specific date patterns (MM/DD or MM-DD)
        date_match = re.search(r"(\d{1,2})[/-](\d{1,2})", text)
        if date_match:
            month, day = date_match.groups()
            return f"{now.year}-{month.zfill(2)}-{day.zfill(2)}"

        # Time of day
        time_mentions = {
            "morning": "09:00",
            "afternoon": "14:00",
            "evening": "18:00",
            "night": "21:00",
        }

        for time_name, time_value in time_mentions.items():
            if time_name in text:
                return f"{now.strftime('%Y-%m-%d')} {time_value}"

        return None

    def validate_intent(self, intent: str) -> bool:
        """Check if intent is valid"""
        valid_intents = set()
        for intents_list in self.INTENT_KEYWORDS.values():
            valid_intents.add(intent)
        return intent in valid_intents or len(intent) > 0

    def get_action_type(self, intent: str) -> str:
        """Map intent to action type"""
        action_map = {
            "task_creation": "create",
            "task_update": "update",
            "task_completion": "complete",
            "task_deletion": "delete",
            "task_list": "list",
            "note_creation": "create",
            "note_search": "search",
            "reminder_creation": "create",
            "email_draft": "draft",
            "knowledge_search": "search",
            "general_question": "answer",
        }
        return action_map.get(intent, "unknown")


# Global parser instance
_parser: IntentParser = None


def get_intent_parser() -> IntentParser:
    """Get or create intent parser"""
    global _parser
    if _parser is None:
        _parser = IntentParser()
    return _parser
