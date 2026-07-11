from pathlib import Path
import os
import re
import textwrap

from app.state_schema import GuideState

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# =====================================================
# PDF STORAGE LOCATION
# Compatible with OpenShift / Docker containers
# =====================================================

GENERATED_GUIDES_DIR = Path(
    os.getenv(
        "GENERATED_GUIDES_DIR",
        "/tmp/generated_guides"
    )
)


GENERATED_GUIDES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


###############################################################################
# Markdown Helpers
###############################################################################

def clean_markdown(text: str) -> str:

    text = textwrap.dedent(text)

    text = re.sub(
        r"^\s+(#{1,6}\s+)",
        r"\1",
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()



def markdown_to_reportlab(text: str) -> str:

    text = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )


    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text
    )


    return text



def build_markdown_table(table_lines):

    styles = getSampleStyleSheet()


    cell_style = styles["BodyText"]

    cell_style.fontSize = 8.5
    cell_style.leading = 10
    cell_style.textColor = colors.black



    header_style = ParagraphStyle(
        "TableHeaderStyle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.white
    )


    rows = []


    for line in table_lines:

        line = line.strip()


        if re.match(
            r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?$",
            line
        ):
            continue


        cells = [

            markdown_to_reportlab(cell.strip())
            if cell.strip()
            else " "

            for cell in line.strip("|").split("|")

        ]


        rows.append(cells)



    if not rows:

        return Spacer(1,0)



    formatted_rows = []


    for row_index, row in enumerate(rows):

        formatted_row = []


        for cell in row:


            if row_index == 0:

                formatted_row.append(
                    Paragraph(
                        cell,
                        header_style
                    )
                )

            else:

                formatted_row.append(
                    Paragraph(
                        cell,
                        cell_style
                    )
                )


        formatted_rows.append(formatted_row)



    column_count = len(
        formatted_rows[0]
    )


    page_width = (
        8.5*inch
        - 0.6*inch
        - 0.6*inch
    )


    col_width = (
        page_width / column_count
    )


    table = Table(
        formatted_rows,
        colWidths=[col_width]*column_count,
        repeatRows=1
    )


    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.HexColor("#1F4E79")
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,0),
                    colors.white
                ),

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "TOP"
                ),
            ]
        )
    )


    return table



###############################################################################
# Page Number
###############################################################################

def add_page_number(canvas, doc):

    canvas.setFont(
        "Helvetica",
        9
    )


    canvas.drawRightString(
        570,
        20,
        f"Page {doc.page}"
    )



###############################################################################
# PDF Generator Node
###############################################################################

def pdf_generator_node(
    state: GuideState
):

    print(
        "------ PDF NODE ------"
    )


    role = state.role


    markdown = clean_markdown(
        state.merge_response
    )


    print(
        markdown[:1500]
    )


    # =================================================
    # FIXED PATH
    # =================================================

    pdf_path = GENERATED_GUIDES_DIR / (
        f"{role.replace(' ', '_')}_Career_Guide.pdf"
    )



    styles = getSampleStyleSheet()


    story = []


    story.append(
        Paragraph(
            f"<b>{role} Career Preparation Guide</b>",
            styles["Title"]
        )
    )


    story.append(
        Spacer(
            1,
            0.35*inch
        )
    )


    lines = markdown.splitlines()


    i = 0


    while i < len(lines):

        line = lines[i].strip()



        if not line:

            story.append(
                Spacer(
                    1,
                    0.12*inch
                )
            )

            i += 1

            continue



        if line.startswith("|"):

            table_lines = []


            while (
                i < len(lines)
                and "|" in lines[i]
            ):

                table_lines.append(
                    lines[i]
                )

                i += 1



            story.append(
                build_markdown_table(
                    table_lines
                )
            )


            story.append(
                Spacer(
                    1,
                    0.2*inch
                )
            )


            continue



        if re.match(
            r"^#{1}(?!#)\s+",
            line
        ):

            title = re.sub(
                r"^#{1}\s+",
                "",
                line
            )


            story.append(
                Paragraph(
                    markdown_to_reportlab(title),
                    styles["Heading1"]
                )
            )


            i += 1

            continue



        if re.match(
            r"^#{2}(?!#)\s+",
            line
        ):

            title = re.sub(
                r"^#{2}\s+",
                "",
                line
            )


            story.append(
                Paragraph(
                    markdown_to_reportlab(title),
                    styles["Heading2"]
                )
            )


            i += 1

            continue
        
        if re.match(
            r"^#{3}(?!#)\s+",
            line
        ):

            title = re.sub(
                r"^#{3}\s+",
                "",
                line
            )


            story.append(
                Paragraph(
                    markdown_to_reportlab(title),
                    styles["Heading3"]
                )
            )


            i += 1

            continue



        if line.startswith("- ") or line.startswith("* "):

            story.append(
                Paragraph(
                    "• " +
                    markdown_to_reportlab(line[2:]),
                    styles["BodyText"]
                )
            )


            i += 1

            continue



        story.append(
            Paragraph(
                markdown_to_reportlab(line),
                styles["BodyText"]
            )
        )


        i += 1



    doc = SimpleDocTemplate(

        str(pdf_path),

        rightMargin=0.6*inch,

        leftMargin=0.6*inch,

        topMargin=0.7*inch,

        bottomMargin=0.7*inch,

    )


    doc.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number,

    )


    print(
        "PDF CREATED:",
        pdf_path
    )


    return {

        "pdf_path": str(pdf_path)

    }