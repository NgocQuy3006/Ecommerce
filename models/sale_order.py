from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ecommerce_platform = fields.Selection([
        ('shopee', 'Shopee'),
        ('lazada', 'Lazada'),
        ('tiktok', 'TikTok'),
    ], string="Platform")

    ecommerce_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipping', 'Shipping'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string="Ecommerce Status")

    def action_sync_ecommerce_orders(self):
        service = self.env['leo.ecommerce.service']
        orders = service.fetch_orders()

        for o in orders:
            partner = self.env['res.partner'].search([
                ('name', '=', o['customer'])
            ], limit=1)

            if not partner:
                partner = self.env['res.partner'].create({
                    'name': o['customer']
                })

            sale = self.create({
                'partner_id': partner.id,
                'client_order_ref': o['name'],
                'ecommerce_platform': o['platform'],
                'ecommerce_status': o.get('status'),
            })

            for line in o['lines']:
                product = self.env['product.product'].search([
                    ('name', '=', line[0])
                ], limit=1)

                if not product:
                    product = self.env['product.product'].create({
                        'name': line[0],
                        'list_price': line[2]
                    })

                self.env['sale.order.line'].create({
                    'order_id': sale.id,
                    'product_id': product.id,
                    'product_uom_qty': line[1],
                    'price_unit': line[2]
                })