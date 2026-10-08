#!/usr/bin/env python3
"""Render the chapter constitution Markdown as TauBetaPiConstitution.pdf.

The web page (constitution.shtml) and this PDF are two renderings of the same
source. Regenerate this whenever the constitution changes so they can't drift.

    python make_constitution_pdf.py "TBP Constitution.md" TauBetaPiConstitution.pdf
"""
import re
import sys

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

MIT_RED = "#750014"
INK = "#1b1b1b"

TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=17, leading=21,
                       textColor=MIT_RED, spaceAfter=3)
SUBTITLE = ParagraphStyle("subtitle", fontName="Helvetica-Oblique", fontSize=10,
                          leading=13, textColor="#555d66", spaceAfter=16)
HEADING = ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=12, leading=15,
                         textColor=MIT_RED, spaceBefore=14, spaceAfter=6, keepWithNext=1)
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                      textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7)
ITEM = ParagraphStyle("item", parent=BODY, spaceAfter=5)


def inline(text):
    """Markdown emphasis and escapes -> reportlab inline markup."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\\([$*_])", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", text)


def build(md_path, out_path):
    lines = open(md_path, encoding="utf-8").read().split("\n")
    story, bullets = [], []

    def flush():
        if bullets:
            story.append(ListFlowable(
                [ListItem(Paragraph(b, ITEM), leftIndent=18) for b in bullets],
                bulletType="bullet", bulletFontSize=7, bulletOffsetY=-1,
                leftIndent=16, spaceAfter=7,
            ))
            bullets.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush()
            continue
        if line.startswith("- "):
            bullets.append(inline(line[2:]))
            continue
        flush()
        if line.startswith("**") and line.endswith("**"):
            story.append(Paragraph(inline(line)[3:-4], TITLE))
        elif line.startswith("*") and line.endswith("*"):
            story.append(Paragraph(inline(line)[3:-4], SUBTITLE))
        elif re.match(r"^Article [IVX]+:", line) or line.endswith(":") and len(line) < 40:
            story.append(Paragraph(inline(line), HEADING))
        else:
            story.append(Paragraph(inline(line), BODY))
    flush()

    doc = SimpleDocTemplate(
        out_path, pagesize=LETTER,
        leftMargin=1 * inch, rightMargin=1 * inch,
        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
        title="Tau Beta Pi Massachusetts Beta Constitution",
        author="MIT Tau Beta Pi, Massachusetts Beta",
    )
    doc.build(story)
    print("wrote", out_path)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
