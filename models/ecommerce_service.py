import requests
import time
import hmac
import hashlib

from odoo import models
from odoo.exceptions import UserError


class EcommerceService(models.AbstractModel):
    _name = 'leo.ecommerce.service'
    _description = 'Ecommerce Service'

 
    def fetch_orders(self):
        shops = self.env['leo.ecommerce.shop'].search([('active', '=', True)])
        orders = []

        for shop in shops:

            # ===== SHOPEE =====
            if shop.platform == 'shopee':
                if not shop.partner_id or not shop.partner_key or not shop.shop_id or not shop.access_token:
                    raise UserError(f"Thiếu config Shopee ở shop: {shop.name}")

                shopee_orders = self._fetch_shopee_orders(shop)
                orders.extend(shopee_orders)

            # ===== LAZADA =====
            elif shop.platform == 'lazada':
                if not shop.app_key or not shop.app_secret or not shop.lazada_access_token:
                    raise UserError(f"Thiếu config Lazada ở shop: {shop.name}")

                lazada_orders = self._fetch_lazada_orders(shop)
                orders.extend(lazada_orders)

            # ===== TIKTOK =====
            elif shop.platform == 'tiktok':
                if not shop.tiktok_app_key or not shop.tiktok_app_secret or not shop.tiktok_access_token:
                    raise UserError(f"Thiếu config TikTok ở shop: {shop.name}")

                tiktok_orders = self._fetch_tiktok_orders(shop)
                orders.extend(tiktok_orders)

        return orders

    # =========================================================
    # SHOPEE
    # =========================================================
    def _fetch_shopee_orders(self, shop):
        base_url = "https://partner.shopeemobile.com"
        path = "/api/v2/order/get_order_list"
        timestamp = int(time.time())

        base_string = f"{shop.partner_id}{path}{timestamp}{shop.access_token}{shop.shop_id}"
        sign = hmac.new(
            shop.partner_key.encode("utf-8"),
            base_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        url = f"{base_url}{path}"
        params = {
            "partner_id": int(shop.partner_id),
            "timestamp": timestamp,
            "access_token": shop.access_token,
            "shop_id": int(shop.shop_id),
            "sign": sign,
            "time_range_field": "create_time",
            "time_from": int(time.time()) - 7 * 24 * 60 * 60,
            "time_to": int(time.time()),
            "page_size": 20,
            "order_status": "READY_TO_SHIP",
        }

        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if response.status_code != 200:
            raise UserError(f"Shopee API lỗi: {response.text}")

        if data.get("error"):
            raise UserError(f"Shopee API lỗi: {data.get('message')}")

        result = []
        order_list = data.get("response", {}).get("order_list", [])

        for order in order_list:
            result.append({
                "name": order.get("order_sn"),
                "customer": "Khách Shopee",
                "platform": "shopee",
                "status": order.get("order_status"),
                "lines": [
                    ["Sản phẩm Shopee", 1, 100000]
                ]
            })

        return result

    # =========================================================
    # LAZADA
    # =========================================================
    def _fetch_lazada_orders(self, shop):
        base_url = "https://api.lazada.vn/rest"
        path = "/orders/get"
        timestamp = str(int(time.time() * 1000))

        params = {
            "app_key": shop.app_key,
            "timestamp": timestamp,
            "sign_method": "sha256",
            "access_token": shop.lazada_access_token,
            "sort_direction": "DESC",
            "offset": "0",
            "limit": "20",
            "created_after": "2026-01-01T00:00:00+07:00",
        }

        sorted_params = sorted(params.items())
        sign_str = path + "".join(f"{k}{v}" for k, v in sorted_params)
        sign = hmac.new(
            shop.app_secret.encode("utf-8"),
            sign_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest().upper()

        params["sign"] = sign

        url = f"{base_url}{path}"
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if response.status_code != 200:
            raise UserError(f"Lazada API lỗi: {response.text}")

        if data.get("code") not in ("0", 0, None):
            raise UserError(f"Lazada API lỗi: {data}")

        result = []
        order_list = data.get("data", {}).get("orders", [])

        for order in order_list:
            result.append({
                "name": str(order.get("order_id")),
                "customer": order.get("customer_first_name") or "Khách Lazada",
                "platform": "lazada",
                "status": "pending",
                "lines": [
                    ["Sản phẩm Lazada", 1, float(order.get("price") or 0)]
                ]
            })

        return result

    # =========================================================
    # TIKTOK
    # =========================================================
    def _fetch_tiktok_orders(self, shop):
        base_url = "https://open-api.tiktokglobalshop.com"
        path = "/api/orders/search"
        timestamp = str(int(time.time()))

        payload = {
            "app_key": shop.tiktok_app_key,
            "timestamp": timestamp,
            "access_token": shop.tiktok_access_token,
            "shop_cipher": shop.shop_cipher or "",
            "page_size": 20,
        }

        sign_str = shop.tiktok_app_secret + path
        for k in sorted(payload.keys()):
            sign_str += f"{k}{payload[k]}"
        sign_str += shop.tiktok_app_secret

        sign = hashlib.sha256(sign_str.encode("utf-8")).hexdigest()
        payload["sign"] = sign

        url = f"{base_url}{path}"
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        if response.status_code != 200:
            raise UserError(f"TikTok API lỗi: {response.text}")

        if data.get("code") not in (0, "0", None):
            raise UserError(f"TikTok API lỗi: {data}")

        result = []
        order_list = data.get("data", {}).get("orders", [])

        for order in order_list:
            result.append({
                "name": str(order.get("order_id")),
                "customer": order.get("buyer_name") or "Khách TikTok",
                "platform": "tiktok",
                "status": order.get("order_status"),
                "lines": [
                    ["Sản phẩm TikTok", 1, float(order.get("payment_total") or 0)]
                ]
            })

        return result
