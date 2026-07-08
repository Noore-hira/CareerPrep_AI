from pathlib import Path
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


###############################################################################
# Markdown Helpers
###############################################################################

def clean_markdown(text: str) -> str:
    """
    Clean LLM generated markdown before PDF conversion.

    Fixes:
    - unwanted indentation before headings
    - broken markdown headings
    - excessive blank lines
    """

    # Remove common indentation
    text = textwrap.dedent(text)

    # Remove spaces before markdown headings
    # Example:
    # "        # Introduction"
    # becomes:
    # "# Introduction"

    text = re.sub(
        r"^\s+(#{1,6}\s+)",
        r"\1",
        text,
        flags=re.MULTILINE
    )

    # Normalize multiple empty lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()



def markdown_to_reportlab(text: str) -> str:
    """
    Convert Markdown inline formatting into ReportLab XML.
    """

    # Escape XML characters safely
    text = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )

    # Bold
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )

    # Italic
    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text
    )

    return text



def build_markdown_table(table_lines):
    """
    Convert markdown table into responsive ReportLab table.
    """
    styles = getSampleStyleSheet()

    # 1. Configure the body cell style safely
    cell_style = styles["BodyText"]
    cell_style.fontSize = 8.5
    cell_style.leading = 10
    cell_style.textColor = colors.black  # Explicitly guarantee body text is black
    
    header_style = ParagraphStyle(
        'TableHeaderStyle',
        parent=styles['BodyText'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    rows = []

    for line in table_lines:


        line = line.strip()


        # Skip markdown separator
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



    ###################################################################
    # Convert strings -> Paragraph
    ###################################################################

    formatted_rows = []


    for row_index,row in enumerate(rows):

        formatted_row=[]


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




    ###################################################################
    # Dynamic column sizing
    ###################################################################

    column_count = len(formatted_rows[0])


    page_width = (
        8.5*inch
        - 0.6*inch
        - 0.6*inch
    )


    col_width = page_width / column_count



    table = Table(
        formatted_rows,
        colWidths=[col_width]*column_count,
        repeatRows=1
    )



    table.setStyle(TableStyle([


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
            "FONTNAME",
            (0,0),
            (-1,0),
            "Helvetica-Bold"
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



        (
            "LEFTPADDING",
            (0,0),
            (-1,-1),
            5
        ),


        (
            "RIGHTPADDING",
            (0,0),
            (-1,-1),
            5
        ),


        (
            "TOPPADDING",
            (0,0),
            (-1,-1),
            5
        ),


        (
            "BOTTOMPADDING",
            (0,0),
            (-1,-1),
            5
        ),


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

    # CLEAN MARKDOWN HERE
    markdown = clean_markdown(state.merge_response)


    print("\n========== CLEANED MARKDOWN ==========\n")
    print(markdown[:1500])
    print("\n======================================\n")


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

    story.append(
        Spacer(1,0.35*inch)
    )



    ###########################################################################
    # Parse Markdown
    ###########################################################################

    lines = markdown.splitlines()

    i = 0


    while i < len(lines):

        line = lines[i].strip()



        if not line:

            story.append(
                Spacer(1,0.12*inch)
            )

            i += 1
            continue



        #######################################################################
        # Table
        #######################################################################

        if line.startswith("|"):

            table_lines=[]

            while (i < len(lines) and "|" in lines[i]):
                table_lines.append(lines[i])
                i+=1


            story.append(
                build_markdown_table(table_lines)
            )

            story.append(
                Spacer(1,0.2*inch)
            )

            continue



        #######################################################################
        # H1
        #######################################################################

        if re.match(r"^#{1}(?!#)\s+", line):

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

            story.append(
                Spacer(1,0.15*inch)
            )

            i += 1
            continue



        #######################################################################
        # H2
        #######################################################################

        if re.match(r"^#{2}(?!#)\s+", line):

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

            story.append(
                Spacer(1,0.10*inch)
            )

            i += 1
            continue



        #######################################################################
        # H3
        #######################################################################

        if re.match(r"^#{3}(?!#)\s+", line):

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


        #######################################################################
        # Bullet
        #######################################################################

        if line.startswith("- ") or line.startswith("* "):

            story.append(
                Paragraph(
                    "• " + markdown_to_reportlab(line[2:]),
                    styles["BodyText"]
                )
            )


            i+=1
            continue



        #######################################################################
        # Numbered List
        #######################################################################

        if re.match(r"^\d+\.", line):

            story.append(
                Paragraph(
                    markdown_to_reportlab(line),
                    styles["BodyText"]
                )
            )


            i+=1
            continue



        #######################################################################
        # Normal Paragraph
        #######################################################################

        story.append(
            Paragraph(
                markdown_to_reportlab(line),
                styles["BodyText"]
            )
        )


        i+=1



    ###########################################################################
    # Build PDF
    ###########################################################################

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


    return {
        "pdf_path": str(pdf_path)
    }