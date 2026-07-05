from app.graph import guide_graph


class GuideService:

    @staticmethod
    def generate(question: str):

        result = guide_graph.invoke({
            "question": question
        })

        print(result)

        if not result.get("continue_pipeline", True):
            return {
                "status": "failed",
                "role": None,
                "response": result.get("response"),
                "pdf_path": None,
            }

        return {
            "status": "success",
            "role": result.get("role"),
            "response": result.get("merge_response"),
            "pdf_path": result.get("pdf_path"),
        }