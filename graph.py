from state_schema import GuideState
from nodes.analyze_request_node import analyze_request_node, analyze_router
from nodes.introduction_RAG import intro_RAG
from nodes.roadmap_RAG import rm_RAG
from nodes.resources_RAG import resources_RAG
from nodes.interview_RAG import interview_RAG
from nodes.projects_RAG import projects_RAG
from nodes.merge import merge
from nodes.PDF_generator import pdf_generator_node
from langgraph.graph import START,END,StateGraph

graph= StateGraph(GuideState)

graph.add_node("Analyze_request",analyze_request_node)
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
        "continue": "Introduction_Section_Generation",
        END: END,
    },
)
graph.add_edge("Analyze_request", "Introduction_Section_Generation")
graph.add_edge("Analyze_request", "Roadmap_Section_Generation")
graph.add_edge("Analyze_request", "Resources_Section_Generation")
graph.add_edge("Analyze_request", "Interview_Questions_Section_Generation")
graph.add_edge("Analyze_request", "Resume_Tips_Section_Generation")
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
#    f.write(png)

#print("Graph saved as langgraph.png")

guide_graph.invoke({"question":"create end to end career guide for Ai Engineer"})