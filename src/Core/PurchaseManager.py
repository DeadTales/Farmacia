import os
from datetime import datetime
from uuid import uuid4

from postgrest.exceptions import APIError

from Core.Compras.Orden_compra import generar_orden_compra
from Core.Response import Response
from Core.Session import Session
from Models.Transaction.TransactionDetail import TransactionDetail
from Models.Vendor import Vendor
from Services.EmailService import EmailService
from Services.Product.ProductRepository import ProductRepository
from Services.Transaction.PurchaseDetailRepository import PurchaseDetailRepository
from Services.Transaction.PurchaseRepository import PurchaseRepository


class PurchaseManager:
    @staticmethod
    def register_purchase(vendor: Vendor, details: list[TransactionDetail], generate_order=True, send_email=False):
        if not vendor or not vendor.vendor_id:
            raise ValueError("Selecciona un proveedor")
        if not details:
            raise ValueError("Agrega al menos un producto")

        try:
            PurchaseManager._validate_details(details)
            subtotal = sum(detail.get_subtotal() for detail in details)
            iva = subtotal * 0.16
            total = subtotal + iva
            purchase_id = PurchaseManager._new_purchase_id()
            user = Session.get_session().user

            PurchaseRepository.create_purchase({
                "purchase_id": purchase_id,
                "date_hout": datetime.now().isoformat(timespec="seconds"),
                "total_purchase": total,
                "vendor_id": vendor.vendor_id,
                "user_id": user.nickname if user else None,
            })
            PurchaseDetailRepository.create_many([
                {
                    "amount": detail.amount,
                    "historical_unit_price": detail.unit_price,
                    "purchase_id": purchase_id,
                    "product_id": detail.product.barcode,
                }
                for detail in details
            ])

            for detail in details:
                ProductRepository.update_stock_and_price(
                    detail.product.barcode,
                    int(detail.product.stock) + int(detail.amount),
                    float(detail.unit_price)
                )

            order_path = PurchaseManager._generate_order(purchase_id, vendor, details) if generate_order or send_email else None
            if send_email:
                if not vendor.email:
                    raise ValueError("El proveedor no tiene correo registrado")
                EmailService.send_pdf(
                    vendor.email,
                    f"Orden de compra Farmacia Si {purchase_id}",
                    "Adjuntamos la orden de compra generada por Farmacia Si.",
                    order_path,
                )
            return Response(
                data={"purchase_id": purchase_id, "subtotal": subtotal, "iva": iva, "total": total, "order_path": order_path},
                message="Compra registrada exitosamente",
                status=200,
            )
        except APIError:
            raise
        except Exception as e:
            print(f"PurchaseManager Error --- {e}")
            raise

    @staticmethod
    def _validate_details(details: list[TransactionDetail]):
        for detail in details:
            if not detail.product or not detail.product.barcode:
                raise ValueError("Hay un producto invalido en la compra")
            if int(detail.amount or 0) <= 0:
                raise ValueError("La cantidad debe ser mayor a cero")
            if float(detail.unit_price or 0) <= 0:
                raise ValueError("El precio debe ser mayor a cero")
            product_data = ProductRepository.get_one(detail.product.barcode)
            if not product_data:
                raise ValueError(f"No existe el producto {detail.product.barcode}")
            detail.product.stock = int(product_data.get("stock") or 0)

    @staticmethod
    def _generate_order(purchase_id, vendor, details):
        output_dir = os.path.abspath(os.path.join(os.getcwd(), "src", "Generated", "Compras"))
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"orden_compra_{purchase_id}.pdf")
        return generar_orden_compra(
            vendor={"name": vendor.name, "phone": vendor.phone, "email": vendor.email},
            productos=[
                {
                    "nombre": detail.product.name,
                    "cantidad": detail.amount,
                    "precio": detail.unit_price,
                    "presentacion": detail.product.description or "General",
                }
                for detail in details
            ],
            numero_orden=purchase_id,
            archivo=path,
        )

    @staticmethod
    def _new_purchase_id():
        return f"C{datetime.now().strftime('%y%m%d%H%M%S')}{uuid4().hex[:4].upper()}"
