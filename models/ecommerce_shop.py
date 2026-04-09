from odoo import models, fields

class EcommerceShop(models.Model):
    _name = 'leo.ecommerce.shop'
    _description = 'Ecommerce Shop'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    platform = fields.Selection([
        ('shopee', 'Shopee'),
        ('lazada', 'Lazada'),
        ('tiktok', 'TikTok'),
    ], required=True)

    # =======================
    # SHOPEE
    # =======================
    partner_id = fields.Char("Shopee Partner ID")
    partner_key = fields.Char("Shopee Partner Key")
    shop_id = fields.Char("Shopee Shop ID")
    access_token = fields.Text("Shopee Access Token")

    # =======================
    # LAZADA
    # =======================
    app_key = fields.Char("Lazada App Key")
    app_secret = fields.Char("Lazada App Secret")
    lazada_access_token = fields.Text("Lazada Access Token")

    # =======================
    # TIKTOK
    # =======================
    tiktok_app_key = fields.Char("TikTok App Key")
    tiktok_app_secret = fields.Char("TikTok App Secret")
    tiktok_access_token = fields.Text("TikTok Access Token")
    shop_cipher = fields.Char("TikTok Shop Cipher")
