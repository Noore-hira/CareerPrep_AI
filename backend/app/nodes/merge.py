import textwrap
from app.state_schema import GuideState

def merge(state: GuideState):
    # This block builds the layout without adding any toxic leading tab spaces
    raw_markdown = f"""
{state.intro_response or ''}

{state.rm_response or ''}

{state.rcs_response or ''}

{state.iv_response or ''}

{state.pj_response or ''}
"""

    # textwrap.dedent cleans any accidental indentation alignment out cleanly
    final_cleaned = textwrap.dedent(raw_markdown).strip()

    return {
        "merge_response": final_cleaned
    }