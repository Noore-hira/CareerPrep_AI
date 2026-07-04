from pathlib import Path
import re
from state_schema import GuideState

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


def pdf_generator_node(state:GuideState) -> GuideState:

    role = state.role
    markdown = state.merge_response

    output_dir = Path("generated_guides")
    output_dir.mkdir(exist_ok=True)

    pdf_path = output_dir / f"{role.replace(' ', '_')}_Career_Guide.pdf"

    styles = getSampleStyleSheet()

    story = []

    # ---------- Cover Title ----------

    story.append(
        Paragraph(
            f"<b>{role} Career Preparation Guide</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    # ---------- Markdown Parsing ----------

    for line in markdown.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 0.12 * inch))
            continue

        # H1
        if line.startswith("# "):
            story.append(
                Paragraph(
                    f"<b>{line[2:]}</b>",
                    styles["Heading1"],
                )
            )
            continue

        # H2
        if line.startswith("## "):
            story.append(
                Paragraph(
                    f"<b>{line[3:]}</b>",
                    styles["Heading2"],
                )
            )
            continue

        # H3
        if line.startswith("### "):
            story.append(
                Paragraph(
                    f"<b>{line[4:]}</b>",
                    styles["Heading3"],
                )
            )
            continue

        # Bullet points
        if line.startswith("- ") or line.startswith("* "):
            story.append(
                Paragraph(
                    "• " + line[2:],
                    styles["BodyText"],
                )
            )
            continue

        # Numbered lists
        if re.match(r"^\d+\.", line):
            story.append(
                Paragraph(
                    line,
                    styles["BodyText"],
                )
            )
            continue

        # Normal paragraph
        story.append(
            Paragraph(
                line,
                styles["BodyText"],
            )
        )

    # ---------- Build PDF ----------

    doc = SimpleDocTemplate(str(pdf_path))

    doc.build(story)

    return state.model_copy(update={"pdf_path": str(pdf_path)})