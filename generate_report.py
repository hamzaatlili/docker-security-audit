
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak
)

# Read actual scan results
with open("report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

findings = report.get("findings", [])
summary = report.get("summary", {})
counts = summary.get("by_severity", {})

output = "docker-security-audit-report.pdf"

NAVY = colors.HexColor("#14243A")
BLUE = colors.HexColor("#2563EB")

severity_colors = {
    "CRITICAL": colors.HexColor("#DC2626"),
    "HIGH": colors.HexColor("#EA580C"),
    "MEDIUM": colors.HexColor("#EAB308"),
    "LOW": colors.HexColor("#16A34A"),
    "INFO": colors.HexColor("#2563EB")
}

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="MainTitle", parent=styles["Title"],
    fontSize=25, textColor=NAVY, spaceAfter=15
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading2"],
    textColor=BLUE, spaceBefore=12, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="SmallText", parent=styles["BodyText"],
    fontSize=8, leading=11
))

doc = SimpleDocTemplate(
    output, pagesize=A4,
    rightMargin=18*mm, leftMargin=18*mm,
    topMargin=18*mm, bottomMargin=18*mm
)

story = []

# Cover
story.append(Spacer(1, 35*mm))
story.append(Paragraph(
    "DOCKER SECURITY AUDIT",
    styles["MainTitle"]
))
story.append(Paragraph(
    "Professional Container Security Assessment Report",
    styles["Heading2"]
))
story.append(Spacer(1, 15*mm))

story.append(Paragraph(
    f"Scanner Version: {report.get('version', 'N/A')}",
    styles["Normal"]
))
story.append(Paragraph(
    f"Scan Date: {report.get('timestamp', 'N/A')}",
    styles["Normal"]
))
story.append(Paragraph(
    f"Total Findings: {len(findings)}",
    styles["Normal"]
))

story.append(PageBreak())

# Executive Summary
story.append(Paragraph("1. Executive Summary", styles["Section"]))

story.append(Paragraph(
    f"The security scan identified {len(findings)} findings "
    "across the scanned Docker environment. "
    "The following table presents their severity distribution.",
    styles["BodyText"]
))
story.append(Spacer(1, 10))

data = [["Severity", "Number of Findings"]]

for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
    data.append([severity, str(counts.get(severity, 0))])

table = Table(data, colWidths=[75*mm, 75*mm])
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("PADDING", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1),
     [colors.white, colors.HexColor("#EFF5FC")]),
]))

story.append(table)
story.append(Spacer(1, 15))

# Detailed Findings
story.append(Paragraph(
    "2. Detailed Security Findings",
    styles["Section"]
))

for i, finding in enumerate(findings, 1):
    severity = str(finding.get("severity", "INFO")).upper()
    color = severity_colors.get(severity, colors.black)

    story.append(Paragraph(
        f'<font color="{color.hexval()}">'
        f'<b>{severity}</b></font> - '
        f'{i}. {finding.get("title", "Untitled")}',
        styles["Heading3"]
    ))

    story.append(Paragraph(
        f"<b>Rule:</b> {finding.get('rule_id', 'N/A')}",
        styles["SmallText"]
    ))

    story.append(Paragraph(
        f"<b>Category:</b> {finding.get('category', 'N/A')}",
        styles["SmallText"]
    ))

    story.append(Paragraph(
        f"<b>Description:</b> {finding.get('description', 'N/A')}",
        styles["SmallText"]
    ))

    story.append(Paragraph(
        f"<b>Remediation:</b> {finding.get('remediation', 'N/A')}",
        styles["SmallText"]
    ))

    story.append(Spacer(1, 8))

# Conclusion
story.append(Paragraph(
    "3. Conclusion & Recommendations",
    styles["Section"]
))

story.append(Paragraph(
    "Prioritize Critical and High findings. "
    "Apply the recommended security configurations, "
    "validate changes, and execute another security scan "
    "to verify remediation.",
    styles["BodyText"]
))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(18*mm, 10*mm, "Docker Security Audit Report")
    canvas.drawRightString(
        A4[0]-18*mm, 10*mm, f"Page {doc.page}"
    )
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)

print(f"PDF created successfully: {output}")
