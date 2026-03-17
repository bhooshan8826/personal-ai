"""
LLM Engine integration with Ollama
"""
import json
import logging
from typing import Dict, List, Optional, Any
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import settings

logger = logging.getLogger(__name__)


class LLMEngine:
    """Local LLM engine using Ollama"""

    def __init__(self):
        """Initialize LLM engine"""
        try:
            self.llm = Ollama(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
                temperature=0.7,
            )
            self.embeddings = OllamaEmbeddings(
                base_url=settings.ollama_base_url,
                model=settings.embedding_model,
            )
            logger.info(f"LLM Engine initialized with model: {settings.ollama_model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM engine: {e}")
            raise

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text from prompt"""
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    def classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify the intent of user input
        Returns: {intent, entities, confidence}
        """
        intent_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
Analyze the user message and classify its intent.

Possible intents:
- task_creation: User wants to create a new task
- task_update: User wants to update a task
- task_completion: User wants to mark a task as done
- task_deletion: User wants to delete a task
- task_list: User wants to see their tasks
- note_creation: User wants to create a note
- note_search: User wants to search notes
- reminder_creation: User wants to set a reminder
- email_draft: User wants help drafting an email
- knowledge_search: User wants to search knowledge base
- general_question: General question or conversation

Extract entities like:
- task: the task description or name
- deadline: when it should be done (e.g., "tomorrow", "Friday", "next week", specific dates)
- priority: high, medium, low
- time: specific time mentions
- note_query: search query for notes

User message: "{text}"

Return ONLY a valid JSON object (no other text):
{{
  "intent": "<intent>",
  "entities": {{}},
  "confidence": 0.0-1.0
}}
""",
        )

        try:
            chain = LLMChain(llm=self.llm, prompt=intent_prompt)
            result = chain.invoke({"text": text})

            # Parse JSON response
            response_text = result.get("text", "")

            # Try to extract JSON from response
            try:
                # Find JSON in response
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                if start != -1 and end > start:
                    json_str = response_text[start:end]
                    parsed = json.loads(json_str)
                    return parsed
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse intent response: {response_text}")

            # Default response if parsing fails
            return {
                "intent": "general_question",
                "entities": {},
                "confidence": 0.5,
            }
        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return {
                "intent": "general_question",
                "entities": {},
                "confidence": 0.0,
            }

    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate contextual response"""
        try:
            full_prompt = self._build_context_prompt(prompt, context)
            response = self.llm.invoke(full_prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error while processing your request."

    def summarize(self, text: str, max_length: int = 500) -> str:
        """Summarize text"""
        prompt = f"""
Summarize the following text concisely in {max_length} characters or less:

{text}

Summary:
"""
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return ""

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        prompt = f"""
Extract structured information from the text. Identify:
- dates/times
- priorities (high/medium/low)
- people names
- actions
- topics

Text: "{text}"

Return as JSON with extracted entities.
"""
        try:
            response = self.llm.invoke(prompt)
            # Try to parse as JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"raw": response}
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}

    def generate_email(
        self,
        subject: str,
        recipient: str,
        tone: str = "professional"
    ) -> str:
        """Draft a professional email"""
        prompt = f"""
Draft a {tone} email with the subject: "{subject}"
To: {recipient}

Email body:
"""
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating email: {e}")
            return ""

    def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for text"""
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []

    def _build_context_prompt(
        self,
        prompt: str,
        context: Optional[Dict] = None
    ) -> str:
        """Build prompt with context"""
        if not context:
            return prompt

        context_str = "\n".join(
            f"{k}: {v}" for k, v in context.items() if v is not None
        )
        return f"""
Context:
{context_str}

Query: {prompt}

Response:
"""

    def health_check(self) -> bool:
        """Check if LLM is accessible"""
        try:
            response = self.llm.invoke("ping")
            return len(response) > 0
        except Exception as e:
            logger.error(f"LLM health check failed: {e}")
            return False


# Global LLM engine instance
_llm_engine: Optional[LLMEngine] = None


def get_llm_engine() -> LLMEngine:
    """Get or create LLM engine"""
    global _llm_engine
    if _llm_engine is None:
        _llm_engine = LLMEngine()
    return _llm_engine


def initialize_llm_engine():
    """Initialize LLM engine"""
    get_llm_engine()
