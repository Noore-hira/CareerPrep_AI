from app.graph import get_graph


class GuideService:

    @staticmethod
    def generate(
        question: str,
        model: str,
        api_key: str,
    ):

        # Lazy load graph only when API is called
        guide_graph = get_graph()

        return guide_graph.invoke(
            {
                "question": question,
                "model": model,
                "api_key": api_key,
            }
        )