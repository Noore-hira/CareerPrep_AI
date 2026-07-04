from typing import Literal
from pydantic import BaseModel, Field
from state_schema import GuideState
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")


class RequestAnalysis(BaseModel):
    intent: Literal["career_guide", "unsupported"] = Field(
        description="Whether the user is requesting a complete career guide."
    )

    role: str | None = Field(
        default=None,
        description="Requested career role if present."
    )

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=groq_api
)

structured_llm = llm.with_structured_output(RequestAnalysis)

analysis_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the request analyzer for CareerPrep AI.

CareerPrep AI ONLY generates COMPLETE career preparation guides.

Supported roles are:

- AI Engineer
- Data Engineer
- Software Engineer
- Full Stack Developer
- DevOps Engineer

Your job:

1. Determine whether the user is requesting a COMPLETE career guide.

Examples of career guide requests:

- Generate a career guide for AI Engineer
- Create a roadmap to become an AI Engineer
- Help me become a DevOps Engineer
- I want to prepare for Software Engineer interviews
- Create an end-to-end guide for Data Engineer

Return:

intent = "career_guide"

and extract the requested role.

--------------------------------------------------

If the user asks for anything else such as:

- Tell me a joke
- Explain Docker
- What is LangGraph
- Give me only interview questions
- Give me only resources
- Give me resume tips only
- What's the weather

Return:

intent = "unsupported"

role = null
"""
        ),
        ("human", "{question}")
    ]
)
analysis_chain = analysis_prompt | structured_llm

SUPPORTED_ROLES = {
    "AI Engineer",
    "Data Engineer",
    "Software Engineer",
    "Full Stack Developer",
    "DevOps Engineer",
}

def analyze_request_node(state: GuideState):
    print("------ ANALYZE REQUEST NODE ------")

    result = analysis_chain.invoke(
        {
            "question": state.question
        }
    )

    # ----------------------------
    # Not a Career Guide Request
    # ----------------------------

    if result.intent == "unsupported":

        return {
            "continue_pipeline": False,

            "response": (
                "CareerPrep AI is designed to generate complete career "
                "preparation guides.\n\n"
                "Currently supported roles are:\n"
                "- AI Engineer\n"
                "- Data Engineer\n"
                "- Software Engineer\n"
                "- Full Stack Developer\n"
                "- DevOps Engineer\n\n"
                "Example:\n"
                "'Generate a complete career guide for AI Engineer.'"
            )
        }

    # ----------------------------
    # Unsupported Role
    # ----------------------------

    if result.role not in SUPPORTED_ROLES:

        return {

            "continue_pipeline": False,

            "response": (
                f"'{result.role}' is currently not supported.\n\n"
                "CareerPrep AI currently supports:\n"
                "- AI Engineer\n"
                "- Data Engineer\n"
                "- Software Engineer\n"
                "- Full Stack Developer\n"
                "- DevOps Engineer"
            )
        }

    # ----------------------------
    # Success
    # ----------------------------

    return {

        "continue_pipeline": True,

        "role": result.role,

        "response": ""
    }


def analyze_router(state: GuideState):

    if state["continue_pipeline"]:
        return "retrievers"

    return END