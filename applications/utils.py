"""
Certificate PDF Generator for Jusoor Platform
Generates volunteer certificates with Arabic text support.
"""

import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display


# Register Arabic-compatible fonts (Arial comes with Windows)
try:
    pdfmetrics.registerFont(TTFont('ArabicFont', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArabicFontBold', 'C:/Windows/Fonts/arialbd.ttf'))
    FONT_REGULAR = 'ArabicFont'
    FONT_BOLD = 'ArabicFontBold'
except Exception:
    FONT_REGULAR = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'


def reshape_arabic(text):
    """Reshape Arabic text so it displays correctly in PDF."""
    if not text:
        return ''
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def generate_certificate_pdf(volunteer_name, opportunity_title, org_name,
                             start_date, end_date, hours, issue_date):
    """
    Generate a volunteer certificate PDF matching the Jusoor template.
    Returns a BytesIO buffer containing the PDF data.
    """
    buffer = io.BytesIO()

    # Landscape A4
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Theme colors
    TEAL = HexColor('#1E3A5F')
    GREEN = HexColor('#4CB944')
    DARK_GREEN = HexColor('#2E7D32')
    GREY = HexColor('#808080')
    LIGHT_GREY = HexColor('#C0C0C0')

    # ===== Outer border =====
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.rect(25, 25, page_width - 50, page_height - 50, stroke=1, fill=0)

    # ===== Jusoor Logo (circular with "J") =====
    logo_x = page_width / 2
    logo_y = page_height - 70
    c.setStrokeColor(DARK_GREEN)
    c.setLineWidth(2.5)
    c.circle(logo_x, logo_y, 25, stroke=1, fill=0)
    c.setFillColor(DARK_GREEN)
    c.setFont(FONT_BOLD, 24)
    c.drawCentredString(logo_x, logo_y - 8, 'J')
    c.setFillColor(TEAL)
    c.setFont(FONT_BOLD, 10)
    c.drawCentredString(logo_x, logo_y - 40, 'JUSOOR')
    c.setFont(FONT_REGULAR, 6)
    c.setFillColor(GREY)
    c.drawCentredString(logo_x, logo_y - 50, 'Turn Your Time Into Experience')

    # ===== Title: شهادة تطوع =====
    c.setFillColor(TEAL)
    c.setFont(FONT_BOLD, 48)
    title = reshape_arabic('شهادة تطوع')
    c.drawCentredString(page_width / 2, page_height - 180, title)

    # ===== Subtitle: تشهد منصة جسور بأن =====
    c.setFillColor(GREY)
    c.setFont(FONT_REGULAR, 14)
    subtitle = reshape_arabic('تشهد منصة جسور بأن')
    c.drawCentredString(page_width / 2, page_height - 225, subtitle)

    # ===== Volunteer name =====
    c.setFillColor(TEAL)
    c.setFont(FONT_BOLD, 38)
    name_display = reshape_arabic(volunteer_name)
    c.drawCentredString(page_width / 2, page_height - 285, name_display)

    # Green underline under name
    name_width = c.stringWidth(name_display, FONT_BOLD, 38)
    c.setStrokeColor(GREEN)
    c.setLineWidth(2)
    underline_half = min(name_width / 2 + 30, 250)
    c.line(page_width / 2 - underline_half, page_height - 298,
           page_width / 2 + underline_half, page_height - 298)

    # ===== Description line 1 =====
    c.setFillColor(TEAL)
    c.setFont(FONT_REGULAR, 15)
    desc1 = reshape_arabic(
        f'قد أنهى فترة التطوع في {opportunity_title} لدى {org_name}،'
    )
    c.drawCentredString(page_width / 2, page_height - 340, desc1)

    # ===== Description line 2 =====
    desc2 = reshape_arabic(
        f'من {start_date} إلى {end_date}، بإجمالي {hours} ساعة تطوعية.'
    )
    c.drawCentredString(page_width / 2, page_height - 368, desc2)

    # ===== Verified seal (centered circle with check) =====
    seal_x = page_width / 2
    seal_y = 150
    c.setStrokeColor(GREEN)
    c.setLineWidth(2)
    c.circle(seal_x, seal_y, 28, stroke=1, fill=0)
    c.setFillColor(GREEN)
    c.setFont(FONT_BOLD, 22)
    c.drawCentredString(seal_x, seal_y + 2, '✓')
    c.setFont(FONT_BOLD, 9)
    verified = reshape_arabic('موثقة')
    c.drawCentredString(seal_x, seal_y - 15, verified)

    # ===== Signature lines =====
    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    # Right line: ممثل المنظمة
    c.line(page_width - 280, 150, page_width - 90, 150)
    c.setFillColor(TEAL)
    c.setFont(FONT_REGULAR, 11)
    rep = reshape_arabic('ممثل المنظمة')
    c.drawCentredString(page_width - 185, 130, rep)
    # Left line: إدارة منصة جسور
    c.line(90, 150, 280, 150)
    admin = reshape_arabic('إدارة منصة جسور')
    c.drawCentredString(185, 130, admin)

    # ===== Issue date =====
    c.setFillColor(TEAL)
    c.setFont(FONT_REGULAR, 10)
    issue = reshape_arabic(f'تاريخ الإصدار: {issue_date}')
    c.drawCentredString(page_width / 2, 85, issue)

    # ===== Decorative bridge pattern at bottom =====
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    y_base = 55
    c.line(40, y_base, page_width - 40, y_base)
    # Vertical pillars
    for i in range(0, int(page_width - 80), 25):
        c.line(50 + i, y_base, 50 + i, y_base - 15)
    c.setStrokeColor(GREEN)
    c.setLineWidth(1.5)
    c.line(40, y_base - 15, page_width - 40, y_base - 15)

    c.save()
    buffer.seek(0)
    return buffer