from pathlib import Path
import re

from state_schema import GuideState

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

###############################################################################
# Markdown Helpers
###############################################################################

def markdown_to_reportlab(text: str) -> str:
    """
    Convert Markdown inline formatting into ReportLab tags.
    """

    # Bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Italic
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)

    return text


def build_markdown_table(table_lines):
    """
    Convert markdown table into ReportLab Table.
    """

    rows = []

    for line in table_lines:

        # Skip separator row
        if re.match(r"^\|\s*-", line):
            continue

        row = [markdown_to_reportlab(cell.strip())
               for cell in line.strip("|").split("|")]

        rows.append(row)

    table = Table(rows, repeatRows=1)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),

        ("BACKGROUND", (0, 1), (-1, -1), colors.white),

        ("ROWBACKGROUNDS",
         (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F6F6F6")]),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("TOPPADDING", (0, 1), (-1, -1), 6),

        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    return table


###############################################################################
# Page Numbers
###############################################################################

def add_page_number(canvas, doc):

    canvas.setFont("Helvetica", 9)

    canvas.drawRightString(
        570,
        20,
        f"Page {doc.page}"
    )


###############################################################################
# PDF Node
###############################################################################

def pdf_generator_node(state: GuideState):

    print("------ PDF NODE ------")

    role = state.role
    markdown = state.merge_response
    print("\n========== RAW MERGED MARKDOWN ==========\n")
    print(markdown[:1500])
    print("\n=========================================\n")

    print("\n========== LINE BY LINE ==========\n")
    for i, line in enumerate(markdown.splitlines()[:40]):
        print(f"{i:02d}: {repr(line)}")
    print("\n===============================\n")

    output_dir = Path("generated_guides")
    output_dir.mkdir(exist_ok=True)

    pdf_path = output_dir / f"{role.replace(' ', '_')}_Career_Guide.pdf"

    styles = getSampleStyleSheet()

    story = []

    ###########################################################################
    # Cover
    ###########################################################################

    story.append(
        Paragraph(
            f"<b>{role} Career Preparation Guide</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 0.35 * inch))

    ###########################################################################
    # Parse Markdown
    ###########################################################################

    lines = markdown.splitlines()

    i = 0

    while i < len(lines):

        line = lines[i].rstrip()

        #######################################################################
        # Blank Line
        #######################################################################

        if not line.strip():
            story.append(Spacer(1, 0.12 * inch))
            i += 1
            continue

        #######################################################################
        # Markdown Table
        #######################################################################

        if line.startswith("|"):

            table_lines = []

            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1

            story.append(build_markdown_table(table_lines))
            story.append(Spacer(1, 0.2 * inch))

            continue

        #######################################################################
        # Horizontal Rule
        #######################################################################

        if line.strip() in ("---", "***"):

            story.append(
                Paragraph(
                    "<font color='grey'>______________________________________________</font>",
                    styles["BodyText"],
                )
            )

            story.append(Spacer(1, 0.15 * inch))

            i += 1
            continue

        #######################################################################
        # H3
        #######################################################################

        if re.match(r"^###\s+", line):

            title = re.sub(r"^###\s+", "", line)

            story.append(
                Paragraph(
                    f"<b>{markdown_to_reportlab(title)}</b>",
                    styles["Heading3"],
                )
            )

            i += 1
            continue


        #######################################################################
        # H2
        #######################################################################

        if re.match(r"^##\s+", line):

            title = re.sub(r"^##\s+", "", line)

            story.append(
                Paragraph(
                    f"<b>{markdown_to_reportlab(title)}</b>",
                    styles["Heading2"],
                )
            )

            story.append(Spacer(1, 0.10 * inch))

            i += 1
            continue


        #######################################################################
        # H1
        #######################################################################

        if re.match(r"^#\s+", line):

            title = re.sub(r"^#\s+", "", line)

            story.append(
                Paragraph(
                    f"<b>{markdown_to_reportlab(title)}</b>",
                    styles["Heading1"],
                )
            )

            story.append(Spacer(1, 0.15 * inch))

            i += 1
            continue

        #######################################################################
        # Bullet List
        #######################################################################

        if line.startswith("- ") or line.startswith("* "):

            story.append(
                Paragraph(
                    "• " + markdown_to_reportlab(line[2:]),
                    styles["BodyText"],
                )
            )

            i += 1
            continue

        #######################################################################
        # Numbered List
        #######################################################################

        if re.match(r"^\d+\.", line):

            story.append(
                Paragraph(
                    markdown_to_reportlab(line),
                    styles["BodyText"],
                )
            )

            i += 1
            continue

        #######################################################################
        # Normal Paragraph
        #######################################################################

        story.append(
            Paragraph(
                markdown_to_reportlab(line),
                styles["BodyText"],
            )
        )

        i += 1

    ###########################################################################
    # Build PDF
    ###########################################################################

    doc = SimpleDocTemplate(
        str(pdf_path),
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    return {"pdf_path": str(pdf_path)}