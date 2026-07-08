from app.graph import guide_graph


class GuideService:

    @staticmethod
    def generate(
        question: str,
        model: str,
        api_key: str,
    ):
        return guide_graph.invoke(
            {
                "question": question,
                "model": model,
                "api_key": api_key,
            }
        )