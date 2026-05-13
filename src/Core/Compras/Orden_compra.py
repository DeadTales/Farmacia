import os
from datetime import datetime, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


PAGE_W, PAGE_H = letter
TEAL = colors.HexColor("#009c8f")
LIGHT_TEAL = colors.HexColor("#e9f8f6")
BORDER = colors.HexColor("#78bdb6")


def generar_orden_compra(vendor, productos, numero_orden, archivo="orden_compra.pdf"):
    c = canvas.Canvas(archivo, pagesize=letter)
    _draw_background(c)

    now = datetime.now()
    delivery = now + timedelta(days=7)
    subtotal = sum(int(p["cantidad"]) * float(p["precio"]) for p in productos)
    iva = subtotal * 0.16
    total = subtotal + iva

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PAGE_W / 2, 535, "ORDEN DE COMPRA")

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(455, 590, "No. OC:")
    c.drawString(455, 565, "Fecha:")
    c.drawString(455, 540, "Hora:")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(510, 590, numero_orden)
    c.drawString(510, 565, now.strftime("%d/%m/%Y"))
    c.drawString(510, 540, now.strftime("%H:%M"))

    _draw_section(c, 40, 400, "DATOS DEL PROVEEDOR", [
        ("Proveedor:", vendor.get("name", "")),
        ("Teléfono:", vendor.get("phone", "")),
        ("Email:", vendor.get("email", "")),
        ("Dirección:", vendor.get("address", "Sin dirección registrada")),
        ("Contacto:", vendor.get("contact", "")),
    ])
    _draw_section(c, 345, 400, "CONDICIONES DE COMPRA", [
        ("Método de pago:", vendor.get("payment_method", "Crédito")),
        ("Términos de pago:", vendor.get("payment_terms", "30 días")),
        ("Fecha de entrega:", delivery.strftime("%d/%m/%Y")),
        ("Lugar de entrega:", "Farmacia Sí - Almacén\nAv. Salud 456, Col. Bienestar\nC.P. 06000, CDMX"),
        ("Observaciones:", "Favor de incluir número\nde orden en la factura."),
    ])

    table = _build_purchase_table(productos)
    table.wrapOn(c, 540, 230)
    table.drawOn(c, 40, 230)

    _draw_notes(c, 40, 105)
    _draw_totals_box(c, 335, 105, subtotal, 0, iva, total)
    _draw_signatures(c, 90, 55)
    _draw_footer(c)
    c.save()
    return archivo


def _build_purchase_table(productos):
    data = [["CANT.", "DESCRIPCIÓN", "PRESENTACIÓN", "PRECIO UNIT.", "SUBTOTAL"]]
    for product in productos[:7]:
        qty = int(product["cantidad"])
        price = float(product["precio"])
        data.append([
            str(qty),
            Paragraph(str(product["nombre"]), _paragraph_style()),
            Paragraph(str(product.get("presentacion", "General")), _paragraph_style()),
            f"${price:,.2f}",
            f"${qty * price:,.2f}",
        ])

    table = Table(data, colWidths=[50, 170, 135, 95, 95], rowHeights=[24] + [31] * (len(data) - 1))
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 1), (2, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfcfcf")),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
    ]))
    return table


def _draw_background(c):
    membrete = _asset_path("Membrete_Farmacia.jpeg")
    if os.path.exists(membrete):
        c.drawImage(membrete, 0, 0, width=PAGE_W, height=PAGE_H)


def _draw_section(c, x, y, title, rows):
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y + 118, title)
    current_y = y + 88
    for label, value in rows:
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, current_y, label)
        c.setFont("Helvetica", 9)
        _draw_multiline(c, str(value), x + 86, current_y, 150, 11)
        current_y -= 28 if "\n" not in str(value) else 48


def _draw_notes(c, x, y):
    c.setStrokeColor(BORDER)
    c.setFillColor(colors.white)
    c.roundRect(x, y, 245, 78, 4, stroke=1, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 12, y + 58, "NOTAS IMPORTANTES")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    notes = [
        "Confirmar existencias antes del envío.",
        "Enviar factura con datos fiscales de Farmacia Sí.",
        "En caso de retraso, favor de avisar con anticipación.",
    ]
    for i, note in enumerate(notes):
        c.drawString(x + 14, y + 40 - (i * 14), f"• {note}")


def _draw_totals_box(c, x, y, subtotal, descuento, iva, total):
    w, h = 235, 105
    c.setStrokeColor(BORDER)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
    c.setFillColor(LIGHT_TEAL)
    c.rect(x, y, 115, h, stroke=0, fill=1)
    rows = [("SUBTOTAL:", subtotal), ("DESCUENTO:", descuento), ("IVA (16%):", iva)]
    row_y = y + h - 24
    for label, value in rows:
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 14, row_y, label)
        c.setFont("Helvetica", 10)
        c.drawRightString(x + w - 16, row_y, f"${float(value):,.2f}")
        row_y -= 25
    c.setStrokeColor(BORDER)
    c.line(x + 14, y + 34, x + w - 14, y + 34)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 14, y + 14, "TOTAL ESTIMADO:")
    c.setFont("Helvetica-Bold", 15)
    c.drawRightString(x + w - 16, y + 14, f"${float(total):,.2f}")


def _draw_signatures(c, x, y):
    c.setStrokeColor(colors.black)
    c.line(x, y, x + 150, y)
    c.line(x + 295, y, x + 445, y)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + 75, y - 12, "ELABORÓ")
    c.drawCentredString(x + 370, y - 12, "AUTORIZÓ")


def _draw_footer(c):
    c.setStrokeColor(BORDER)
    c.line(40, 35, 572, 35)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(PAGE_W / 2, 20, "Farmacia Sí - Donde sí te alcanza")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 8, "Av. Salud 456, Col. Bienestar, C.P. 06000, CDMX  |  Tel. 55 9876 5432")


def _draw_multiline(c, text, x, y, width, leading):
    for idx, line in enumerate(text.splitlines() or [""]):
        paragraph = Paragraph(line, _paragraph_style(font_size=8.5, leading=leading))
        paragraph.wrapOn(c, width, 20)
        paragraph.drawOn(c, x, y - (idx * leading))


def _paragraph_style(font_size=8.5, leading=10):
    return ParagraphStyle("normal-small", fontName="Helvetica", fontSize=font_size, leading=leading)


def _asset_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, "..", "..", "Assets", "images", filename))
