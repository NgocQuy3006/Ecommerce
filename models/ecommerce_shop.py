from odoo import models, fields

class EcommerceShop(models.Model):
    _name = 'leo.ecommerce.shop'
    _description = 'Ecommerce Shop'

    name = fields.Char(required=True)
    platform = fields.Selection([
        ('shopee', 'Shopee'),
        ('lazada', 'Lazada'),
        ('tiktok', 'TikTok'),
    ], required=True)

    # Shopee
    partner_id = fields.Char()
    partner_key = fields.Char()
    shop_id = fields.Char()

    # Lazada
    app_key = fields.Char()
    app_secret = fields.Char()

    # TikTok
    tiktok_app_key = fields.Char()
    tiktok_app_secret = fields.Char()

    active = fields.Boolean(default=True)