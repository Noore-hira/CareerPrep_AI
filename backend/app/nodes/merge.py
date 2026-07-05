from app.state_schema import GuideState
def merge(state: GuideState):

    final = f"""
        {state.intro_response}

        ---

        {state.rm_response}

        ---

        {state.rcs_response}

        ---

        {state.iv_response}

        ---

        {state.pj_response}
        """

    return {
        "merge_response": final
    }