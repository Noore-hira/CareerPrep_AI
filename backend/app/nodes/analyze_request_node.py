from typing import Literal

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END

from app.state_schema import GuideState
from app.prompts.prompts import analysis_prompt



###############################################################################
# Structured Output Schema
###############################################################################

class RequestAnalysis(BaseModel):

    intent: Literal[
        "career_guide",
        "unsupported"
    ] = Field(
        description="Whether the user wants a complete career preparation guide."
    )


    role: Literal[
        "AI Engineer",
        "Data Engineer",
        "Software Engineer",
        "FullStack Developer",
        "DevOps Engineer",
        None
    ] = Field(
        default=None,
        description=(
            "Canonical supported career role. "
            "Must exactly match one of the supported roles."
        )
    )



###############################################################################
# Supported Roles
###############################################################################

SUPPORTED_ROLES = {
    "AI Engineer",
    "Data Engineer",
    "Software Engineer",
    "FullStack Developer",
    "DevOps Engineer",
}



###############################################################################
# Analyze Request Node
###############################################################################

def analyze_request_node(state: GuideState):

    print("------ ANALYZE REQUEST NODE ------")


    llm = ChatGroq(
        model=state.model,
        api_key=state.api_key,
        temperature=0,
    )


    structured_llm = llm.with_structured_output(
        RequestAnalysis
    )


    analysis_chain = (
        analysis_prompt 
        | structured_llm
    )


    result = analysis_chain.invoke(
        {
            "question": state.question
        }
    )


    print("LLM CLASSIFICATION:")
    print(result)



    ###########################################################################
    # Not a Career Guide Request
    ###########################################################################

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
                "- FullStack Developer\n"
                "- DevOps Engineer\n\n"

                "Example:\n"
                "'Generate a complete career guide for AI Engineer.'"
            )
        }



    ###########################################################################
    # Role Validation
    ###########################################################################

    if result.role not in SUPPORTED_ROLES:

        return {

            "continue_pipeline": False,

            "response": (
                f"'{result.role}' is currently not supported.\n\n"

                "CareerPrep AI currently supports:\n"
                "- AI Engineer\n"
                "- Data Engineer\n"
                "- Software Engineer\n"
                "- FullStack Developer\n"
                "- DevOps Engineer"
            )
        }



    ###########################################################################
    # Success
    ###########################################################################

    return {

        "continue_pipeline": True,

        # IMPORTANT:
        # This value exactly matches vector DB metadata
        "role": result.role,

        "response": ""
    }



###############################################################################
# Router
###############################################################################

def analyze_router(state: GuideState):

    if state.continue_pipeline:
        return "continue"

    return END