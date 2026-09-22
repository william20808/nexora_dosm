from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from build_part2_literature_review import REFERENCES, SECTIONS


OUT = Path(__file__).with_name("_qa_part2_layout.pdf")

styles = getSampleStyleSheet()
body = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Times-Roman",
    fontSize=12,
    leading=18,
    alignment=TA_JUSTIFY,
    spaceAfter=0,
)
heading = ParagraphStyle(
    "Heading",
    parent=body,
    fontName="Times-Bold",
    alignment=TA_LEFT,
    keepWithNext=True,
    spaceBefore=6,
    spaceAfter=2,
)
reference = ParagraphStyle(
    "Reference",
    parent=body,
    fontSize=12,
    leading=18,
    alignment=TA_LEFT,
    leftIndent=1.27 * cm,
    firstLineIndent=-1.27 * cm,
    spaceAfter=0,
)

story = [Paragraph("2.0 LITERATURE REVIEW", heading)]
for title, paragraphs in SECTIONS:
    story.append(Paragraph(title, heading))
    for text in paragraphs:
        story.append(Paragraph(text, body))

story.extend([PageBreak(), Paragraph("REFERENCES", heading)])
for item in REFERENCES:
    story.append(Paragraph(item, reference))

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2.0 * cm,
    rightMargin=2.0 * cm,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm,
    title="Part 2 Literature Review QA Render",
)
doc.build(story)
print(OUT)
