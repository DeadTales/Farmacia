from Services.Connection import db
from postgrest.exceptions import APIError
from Models.Vendor import Vendor

class VendorRepositoy:
    table_name = ""
    params = {}
    @staticmethod
    def get_all():
        try:
            response = db.table("vendor").select("*").execute()

            data = response.data

            if not data:
                return None
            
            return data

        except APIError as e:
            print(f"VendorRepository Error: {e.message}")
            raise Exception(e.message)
    
    @staticmethod
    def get_one(id):
        try:
            response = db.table("vendor").select("*").eq("vendor_id", id).single().execute()

            data = response.data

            if not data:
                return None
            
            return data
        except APIError as e:
            print(f"VendorRepository Error: {e.message}")
            raise Exception(e.message)
    
    @staticmethod
    def create(vendor: Vendor):  
        try:
            response = db.table("vendor").insert(vendor.to_dict()).execute()

            return response.data
        except APIError as e:
            print(f"VendorRepository Error: {e.message}")
            raise Exception(e.message)

    @staticmethod
    def update(vendor: Vendor, id):
        try:
            response = db.table("vendor").update(vendor.to_dict()).eq("vendor_id", id)

            return response.data
        except APIError as e:
            print(f"VendorRepository-Error: {e.message}")
            raise Exception(e.message)
    
    @staticmethod
    def delete(id):
        try:
            response = db.table("vendor")