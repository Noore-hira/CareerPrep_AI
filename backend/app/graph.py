from app.state_schema import GuideState
from app.nodes.analyze_request_node import analyze_request_node, analyze_router
from app.nodes.introduction_RAG import intro_RAG
from app.nodes.roadmap_RAG import rm_RAG
from app.nodes.resources_RAG import resources_RAG
from app.nodes.interview_RAG import interview_RAG
from app.nodes.projects_RAG import projects_RAG
from app.nodes.merge import merge
from app.nodes.PDF_generator import pdf_generator_node
from langgraph.graph import START,END,StateGraph

def parallel_start(state: GuideState):
    return {}

graph= StateGraph(GuideState)

graph.add_node("Analyze_request",analyze_request_node)
graph.add_node("Parallel_Start", parallel_start)
graph.add_node("Introduction_Section_Generation",intro_RAG)
graph.add_node("Roadmap_Section_Generation",rm_RAG)
graph.add_node("Resources_Section_Generation",resources_RAG)
graph.add_node("Interview_Questions_Section_Generation",interview_RAG)
graph.add_node("Resume_Tips_Section_Generation",projects_RAG)
graph.add_node("Merge_Sections",merge)
graph.add_node("PDF",pdf_generator_node)

graph.add_edge(START,"Analyze_request")
graph.add_conditional_edges(
    "Analyze_request",
    analyze_router,
    {
        "continue": "Parallel_Start",
        END: END,
    },
)
graph.add_edge("Parallel_Start", "Introduction_Section_Generation")
graph.add_edge("Parallel_Start", "Roadmap_Section_Generation")
graph.add_edge("Parallel_Start", "Resources_Section_Generation")
graph.add_edge("Parallel_Start", "Interview_Questions_Section_Generation")
graph.add_edge("Parallel_Start", "Resume_Tips_Section_Generation")
graph.add_edge("Introduction_Section_Generation", "Merge_Sections")
graph.add_edge("Roadmap_Section_Generation", "Merge_Sections")
graph.add_edge("Resources_Section_Generation", "Merge_Sections")
graph.add_edge("Interview_Questions_Section_Generation", "Merge_Sections")
graph.add_edge("Resume_Tips_Section_Generation", "Merge_Sections")
graph.add_edge("Merge_Sections", "PDF")
graph.add_edge("PDF", END)
guide_graph=graph.compile()

#png=guide_graph.get_graph().draw_mermaid_png()
#with open("langgraph.png", "wb") as f:
    #f.write(png)

#print("Graph saved as langgraph.png")

#result=guide_graph.invoke({"question":"give me end to end Software engineer career guide"})
#print(result)