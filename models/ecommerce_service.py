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
                if not shop.partner_id or not shop.partner_key or not shop.shop_id:
                    raise UserError("Thiếu config Shopee")

                shopee_orders = self._fetch_shopee_orders(shop)
                orders.extend(shopee_orders)

            # ===== LAZADA =====
            elif shop.platform == 'lazada':
                if not shop.app_key or not shop.app_secret:
                    raise UserError("Thiếu config Lazada")

                lazada_orders = self._fetch_lazada_orders(shop)
                orders.extend(lazada_orders)

            # ===== TIKTOK =====
            elif shop.platform == 'tiktok':
                if not shop.tiktok_app_key or not shop.tiktok_app_secret:
                    raise UserError("Thiếu config TikTok")

                tiktok_orders = self._fetch_tiktok_orders(shop)
                orders.extend(tiktok_orders)

        return orders

    # ================= API HANDLER =================

    def _fetch_shopee_orders(self, shop):

        return []

    def _fetch_lazada_orders(self, shop):

        return []

    def _fetch_tiktok_orders(self, shop):

        return []