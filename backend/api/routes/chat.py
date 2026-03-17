"""
Chat API routes
"""
import uuid
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import ChatRequest, ChatResponse, IntentResponse
from core.intent_parser import get_intent_parser
from core.llm_engine import get_llm_engine
from database.models import ConversationHistory

router = APIRouter(prefix="/api/v1", tags=["chat"])
intent_parser = get_intent_parser()
llm_engine = get_llm_engine()


@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Handle chat message"""
    user_id = "default-user"
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # Parse intent
    intent_result = intent_parser.parse(request.message)
    intent = intent_result.get("intent", "general_question")
    entities = intent_result.get("entities", {})

    # Generate response
    response_text = llm_engine.generate_response(
        request.message,
        context={
            "intent": intent,
            "entities": entities,
        }
    )

    # Save conversation history
    user_msg = ConversationHistory(
        id=str(uuid.uuid4()),
        user_id=user_id,
        role="user",
        content=request.message,
        context=intent_result
    )
    db.add(user_msg)

    assistant_msg = ConversationHistory(
        id=str(uuid.uuid4()),
        user_id=user_id,
        role="assistant",
        content=response_text,
        context={"intent": intent}
    )
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(
        id=conversation_id,
        response=response_text,
        intent=intent,
        entities=entities,
        actions=[]
    )


@router.post("/intent", response_model=IntentResponse)
async def analyze_intent(request: ChatRequest):
    """Analyze intent of a message"""
    result = intent_parser.parse(request.message)

    return IntentResponse(
        intent=result.get("intent", "general_question"),
        entities=result.get("entities", {}),
        confidence=result.get("confidence", 0.0)
    )


@router.websocket("/chat/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    user_id = "default-user"

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "")

            if not message:
                continue

            # Parse intent
            intent_result = intent_parser.parse(message)
            intent = intent_result.get("intent", "general_question")
            entities = intent_result.get("entities", {})

            # Generate response
            response_text = llm_engine.generate_response(
                message,
                context={
                    "intent": intent,
                    "entities": entities,
                }
            )

            # Send response
            await websocket.send_json({
                "response": response_text,
                "intent": intent,
                "entities": entities,
            })

    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
    except Exception as e:
        await websocket.send_json({
            "error": str(e)
        })
        await websocket.close()
