import requests


class AddressApiService:
    MEXICO_API_URL = "https://mexico-api.devaleff.com/api/codigo-postal"
    SEPOMEX_URL = "https://sepomex.icalialabs.com/api/v1/zip_codes"
    ZIPPOPOTAM_URL = "https://api.zippopotam.us/mx"

    @classmethod
    def get_by_postal_code(cls, postal_code: str) -> dict:
        cp = (postal_code or "").strip()
        if len(cp) != 5 or not cp.isdigit():
            raise ValueError("El codigo postal debe tener 5 digitos")

        for source in (cls._get_from_mexico_api, cls._get_from_sepomex, cls._get_from_zippopotam):
            try:
                data = source(cp)
                if data.get("settlements"):
                    return data
            except requests.RequestException:
                continue

        return {"postal_code": cp, "state": "", "city": "", "municipality": "", "settlements": []}

    @classmethod
    def _get_from_mexico_api(cls, cp: str) -> dict:
        response = requests.get(f"{cls.MEXICO_API_URL}/{cp}", params={"per_page": 200}, timeout=6)
        response.raise_for_status()
        payload = response.json()
        rows = payload.get("data", [])
        if not rows:
            return {"postal_code": cp, "state": "", "city": "", "municipality": "", "settlements": []}

        first = rows[0]
        municipality = cls._pick(first, "D_mnpio", "d_mnpio", "municipality", "municipio")
        settlements = sorted({
            cls._pick(row, "d_asenta", "settlement", "asentamiento", "colonia", "name")
            for row in rows
            if cls._pick(row, "d_asenta", "settlement", "asentamiento", "colonia", "name")
        })

        return {
            "postal_code": cp,
            "state": cls._pick(first, "d_estado", "state", "estado"),
            "city": municipality or cls._pick(first, "d_ciudad", "city", "ciudad"),
            "municipality": municipality,
            "settlements": settlements,
        }

    @classmethod
    def _get_from_sepomex(cls, cp: str) -> dict:
        response = requests.get(cls.SEPOMEX_URL, params={"zip_code": cp, "per_page": 200}, timeout=6)
        response.raise_for_status()
        payload = response.json()
        rows = payload.get("zip_codes", []) or payload.get("zipCodes", [])
        if not rows:
            return {"postal_code": cp, "state": "", "city": "", "municipality": "", "settlements": []}

        first = rows[0]
        settlements = sorted({
            cls._pick(row, "d_asenta", "settlement", "asentamiento", "name")
            for row in rows
            if cls._pick(row, "d_asenta", "settlement", "asentamiento", "name")
        })

        return {
            "postal_code": cp,
            "state": cls._pick(first, "d_estado", "state", "estado"),
            "city": cls._pick(first, "D_mnpio", "d_mnpio", "municipality", "municipio") or cls._pick(first, "d_ciudad", "city", "ciudad"),
            "municipality": cls._pick(first, "D_mnpio", "d_mnpio", "municipality", "municipio"),
            "settlements": settlements,
        }

    @classmethod
    def _get_from_zippopotam(cls, cp: str) -> dict:
        response = requests.get(f"{cls.ZIPPOPOTAM_URL}/{cp}", timeout=6)
        if response.status_code == 404:
            return {"postal_code": cp, "state": "", "city": "", "settlements": []}
        response.raise_for_status()

        payload = response.json()
        places = payload.get("places", [])
        settlements = sorted({place.get("place name", "") for place in places if place.get("place name")})
        first_place = places[0] if places else {}

        return {
            "postal_code": payload.get("post code", cp),
            "state": first_place.get("state", ""),
            "city": first_place.get("county", ""),
            "municipality": first_place.get("county", ""),
            "settlements": settlements,
        }

    @staticmethod
    def _pick(data: dict, *keys: str) -> str:
        for key in keys:
            value = data.get(key)
            if value:
                return str(value)
        return ""
