from pydantic import BaseModel

class GuideState(BaseModel):
    question:str 
    intro_refined_ques:str =""
    rcs_refined_ques:str =""
    rm_refined_ques:str=""
    iv_refined_ques:str=""
    pj_refined_ques:str=""
    intro_response:str=""
    rcs_response:str=""
    rm_response:str=""
    iv_response:str=""
    pj_response:str=""