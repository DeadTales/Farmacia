import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


PAGE_W, PAGE_H = letter
TEAL = colors.HexColor("#009c8f")
LIGHT_TEAL = colors.HexColor("#e9f8f6")
BORDER = colors.HexColor("#78bdb6")


def generar_factura(nombre_cliente, rfc, productos, total, archivo_salida="factura.pdf",
                    numero_factura=None, descuento=0, puntos_generados=0,
                    telefono="", correo="", direccion="", metodo_pago="Efectivo"):
    c = canvas.Canvas(archivo_salida, pagesize=letter)
    _draw_background(c)

    now = datetime.now()
    subtotal = sum(int(p["cantidad"]) * float(p["precio"]) for p in productos)
    iva = 0.0
    total_final = float(total)

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, 525, "FACTURA")

    c.setFillColor(colors.black)
    _draw_label_value(c, 40, 495, "Folio:", numero_factura or "N/A")
    _draw_label_value(c, 40, 472, "Fecha:", now.strftime("%d/%m/%Y %H:%M"))
    _draw_label_value(c, 40, 449, "Método de pago:", metodo_pago)
    _draw_label_value(c, 40, 426, "Forma de pago:", "Pago en una sola exhibición")
    _draw_label_value(c, 40, 403, "Uso de CFDI:", "G03 - Gastos en general")

    _draw_info_box(c, 330, 382, 230, 165, "DATOS DEL CLIENTE", [
        ("Nombre:", nombre_cliente),
        ("RFC:", rfc or "XAXX010101000"),
        ("Dirección:", direccion or "Sin dirección registrada"),
        ("Teléfono:", telefono or "N/A"),
        ("Correo:", correo or "N/A"),
    ])

    table_y = 235
    table = _build_products_table(productos, ["CANT.", "DESCRIPCIÓN", "PRECIO UNIT.", "SUBTOTAL"],
                                  [55, 255, 125, 120])
    table.wrapOn(c, 555, 260)
    table.drawOn(c, 38, table_y)

    _draw_total_letters(c, 40, 150, total_final)
    _draw_totals_box(c, 355, 75, subtotal, descuento, iva, total_final, "TOTAL:")
    _draw_thanks(c, 40, 65, "¡GRACIAS POR SU COMPRA!", "Cuida tu salud, estamos para servirte.")
    _draw_footer(c)

    c.save()
    return archivo_salida


def _build_products_table(productos, headers, widths):
    data = [headers]
    for product in productos[:8]:
        qty = int(product["cantidad"])
        price = float(product["precio"])
        data.append([
            str(qty),
            Paragraph(str(product["nombre"]), _paragraph_style()),
            f"${price:,.2f}",
            f"${qty * price:,.2f}",
        ])

    table = Table(data, colWidths=widths, rowHeights=[24] + [40] * (len(data) - 1))
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfcfcf")),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
    ]))
    return table


def _draw_background(c):
    membrete = _asset_path("Membrete_Farmacia.jpeg")
    if os.path.exists(membrete):
        c.drawImage(membrete, 0, 0, width=PAGE_W, height=PAGE_H)


def _draw_label_value(c, x, y, label, value):
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, label)
    c.setFont("Helvetica", 10)
    c.drawString(x + 100, y, str(value))


def _draw_info_box(c, x, y, w, h, title, rows):
    c.setStrokeColor(BORDER)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#55bfb4"))
    c.roundRect(x, y + h - 24, w, 24, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + w / 2, y + h - 17, title)

    text_y = y + h - 48
    for label, value in rows:
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 14, text_y, label)
        c.setFont("Helvetica", 9)
        _draw_wrapped(c, str(value), x + 88, text_y, w - 102, 10)
        text_y -= 26


def _draw_total_letters(c, x, y, total):
    c.setStrokeColor(BORDER)
    c.setFillColor(colors.white)
    c.roundRect(x, y, 285, 48, 4, stroke=1, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 12, y + 31, "TOTAL CON LETRA")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(x + 12, y + 14, _money_text(total))


def _draw_totals_box(c, x, y, subtotal, descuento, iva, total, total_label):
    w, h = 220, 125
    c.setStrokeColor(BORDER)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
    c.setFillColor(LIGHT_TEAL)
    c.rect(x, y, 115, h, stroke=0, fill=1)

    rows = [("SUBTOTAL:", subtotal), ("DESCUENTO:", descuento), ("IVA (16%):", iva)]
    row_y = y + h - 26
    for label, value in rows:
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 12, row_y, label)
        c.setFont("Helvetica", 10)
        c.drawRightString(x + w - 18, row_y, f"${float(value):,.2f}")
        row_y -= 27

    c.setStrokeColor(BORDER)
    c.line(x + 12, y + 42, x + w - 12, y + 42)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 12, y + 18, total_label)
    c.setFont("Helvetica-Bold", 15)
    c.drawRightString(x + w - 18, y + 18, f"${float(total):,.2f}")


def _draw_thanks(c, x, y, title, subtitle):
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 95, y + 30, title)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(x + 95, y + 12, subtitle)
    c.setFillColor(colors.HexColor("#d7f5f1"))
    for i, txt in enumerate(["f", "ig", "wa"]):
        c.circle(x + 105 + (i * 28), y - 12, 9, stroke=0, fill=1)
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(x + 105 + (i * 28), y - 15, txt)
        c.setFillColor(colors.HexColor("#d7f5f1"))


def _draw_footer(c):
    c.setStrokeColor(BORDER)
    c.line(40, 42, 572, 42)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(PAGE_W / 2, 24, "Farmacia Sí - Donde sí te alcanza")
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 12, "Av. Salud 456, Col. Bienestar, C.P. 06000, CDMX  |  Tel. 55 9876 5432")


def _draw_wrapped(c, text, x, y, width, leading):
    paragraph = Paragraph(text, _paragraph_style(font_size=8.5, leading=leading))
    paragraph.wrapOn(c, width, 40)
    paragraph.drawOn(c, x, y - paragraph.height + 8)


def _paragraph_style(font_size=9, leading=11):
    return ParagraphStyle("normal-small", fontName="Helvetica", fontSize=font_size, leading=leading)


def _money_text(total):
    pesos = int(total)
    cents = int(round((float(total) - pesos) * 100))
    return f"{pesos:,} pesos {cents:02d}/100 M.N."


def _asset_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, "..", "..", "Assets", "images", filename))
