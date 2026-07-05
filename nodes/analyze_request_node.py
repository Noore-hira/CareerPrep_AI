from typing import Literal
from pydantic import BaseModel, Field
from state_schema import GuideState
from langchain_groq import ChatGroq
from langgraph.graph import END
from prompts.prompts import analysis_prompt
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
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=groq_api
)

structured_llm = llm.with_structured_output(RequestAnalysis)

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

    if state.continue_pipeline:
        return "continue"

    return END