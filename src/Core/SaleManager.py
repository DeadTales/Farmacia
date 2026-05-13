import os
from datetime import datetime
from uuid import uuid4

from postgrest.exceptions import APIError

from Core.ClientManager import ClientManager
from Core.Factura.Facturacion import generar_factura
from Core.Response import Response
from Core.Session import Session
from Models.Client import Client
from Models.Transaction.TransactionDetail import TransactionDetail
from Services.ClientRepository import ClientRepository
from Services.EmailService import EmailService
from Services.Product.ProductRepository import ProductRepository
from Services.Transaction.SaleDetailRepository import SaleDetailRepository
from Services.Transaction.SaleRepository import SaleRepository


class SaleManager:
    POINTS_THRESHOLD = 500
    POINTS_PER_PURCHASE = 10
    DISCOUNT_POINTS = 50
    DISCOUNT_RATE = 0.10

    @staticmethod
    def register_sale(client: Client, details: list[TransactionDetail], invoice=False, send_email=False):
        if not client or not client.email:
            raise ValueError("Selecciona o registra un cliente")
        if not details:
            raise ValueError("Agrega al menos un producto")

        try:
            current_client = SaleManager._ensure_client(client)
            SaleManager._validate_details(details)

            subtotal = sum(detail.get_subtotal() for detail in details)
            earned_points = SaleManager.POINTS_PER_PURCHASE if subtotal > SaleManager.POINTS_THRESHOLD else 0
            current_points = current_client.points or 0
            discount = subtotal * SaleManager.DISCOUNT_RATE if current_points + earned_points >= SaleManager.DISCOUNT_POINTS else 0
            total = subtotal - discount
            new_points = 0 if discount else current_points + earned_points

            sale_id = SaleManager._new_sale_id()
            user = Session.get_session().user
            SaleRepository.create_sale({
                "sale_id": sale_id,
                "date_hour": datetime.now().isoformat(timespec="seconds"),
                "total_sale": total,
                "client_id": current_client.email,
                "user_id": user.nickname if user else None,
            })

            SaleDetailRepository.create_many([
                {
                    "amount": detail.amount,
                    "historical_price_unit": detail.unit_price,
                    "sale_id": sale_id,
                    "product_id": detail.product.barcode,
                }
                for detail in details
            ])

            for detail in details:
                ProductRepository.update_stock(detail.product.barcode, int(detail.product.stock) - int(detail.amount))

            ClientRepository.update(current_client.email, {
                "email": current_client.email,
                "first_name": current_client.first_name,
                "last_name": current_client.last_name,
                "rfc": current_client.rfc,
                "phone": current_client.phone,
                "points": new_points,
            })

            invoice_path = None
            if invoice:
                invoice_path = SaleManager._generate_invoice(sale_id, current_client, details, total, discount, earned_points)
                if send_email:
                    EmailService.send_invoice(
                        current_client.email,
                        f"Factura Farmacia Si {sale_id}",
                        "Adjuntamos la factura de tu compra. Gracias por tu preferencia.",
                        invoice_path,
                    )

            return Response(
                data={
                    "sale_id": sale_id,
                    "subtotal": subtotal,
                    "discount": discount,
                    "total": total,
                    "earned_points": earned_points,
                    "new_points": new_points,
                    "invoice_path": invoice_path,
                },
                message="Venta registrada exitosamente",
                status=200,
            )
        except APIError:
            raise
        except Exception as e:
            print(f"SaleManager Error --- {e}")
            raise

    @staticmethod
    def _ensure_client(client: Client):
        try:
            data = ClientRepository.get_one(client.email)
            if data:
                existing = Client.from_dict(data)
                existing.rfc = existing.rfc or client.rfc
                existing.phone = existing.phone or client.phone
                return existing
        except APIError:
            pass

        ClientManager.create_client(client)
        return client

    @staticmethod
    def _validate_details(details: list[TransactionDetail]):
        for detail in details:
            if not detail.product or not detail.product.barcode:
                raise ValueError("Hay un producto invalido en la venta")
            if int(detail.amount or 0) <= 0:
                raise ValueError("La cantidad debe ser mayor a cero")
            if float(detail.unit_price or 0) <= 0:
                raise ValueError("El precio debe ser mayor a cero")
            product_data = ProductRepository.get_one(detail.product.barcode)
            current_stock = int(product_data.get("stock") or 0) if product_data else 0
            detail.unit_price = float(product_data.get("price") or detail.unit_price or 0)
            if int(detail.amount) > current_stock:
                raise ValueError(f"Stock insuficiente para {detail.product.name}. Disponible: {current_stock}")
            detail.product.stock = current_stock
            detail.product.price = detail.unit_price

    @staticmethod
    def _generate_invoice(sale_id, client, details, total, discount, earned_points):
        output_dir = os.path.abspath(os.path.join(os.getcwd(), "src", "Generated", "Facturas"))
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"factura_{sale_id}.pdf")
        return generar_factura(
            nombre_cliente=f"{client.first_name} {client.last_name}",
            rfc=client.rfc,
            productos=[
                {
                    "nombre": detail.product.name,
                    "cantidad": detail.amount,
                    "precio": detail.unit_price,
                }
                for detail in details
            ],
            total=total,
            archivo_salida=path,
            numero_factura=sale_id,
            descuento=discount,
            puntos_generados=earned_points,
            telefono=client.phone,
            correo=client.email,
            direccion=SaleManager._format_address(client.address),
        )

    @staticmethod
    def _format_address(address):
        if hasattr(address, "get_settlement"):
            settlement = address.get_settlement()
            city = settlement.get_cat_city() if settlement else None
            state = city.get_cat_state() if city else None
            parts = [
                address.get_street(),
                address.get_ext_num(),
                settlement.get_name() if settlement else "",
                city.get_name() if city else "",
                state.get_name() if state else "",
            ]
            return ", ".join([part for part in parts if part])
        if isinstance(address, dict):
            parts = [
                address.get("street"),
                address.get("external_number"),
                address.get("settlement"),
                address.get("city"),
                address.get("state"),
                address.get("postal_code"),
            ]
            return ", ".join([part for part in parts if part])
        return ""

    @staticmethod
    def _new_sale_id():
        return f"V{datetime.now().strftime('%y%m%d%H%M%S')}{uuid4().hex[:4].upper()}"
