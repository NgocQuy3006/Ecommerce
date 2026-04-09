{
    'name': 'Leo Ecommerce Connector',
    'version': '1.0',
    'summary': 'Connect Shopee, Lazada, TikTok to Sale Order',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/ecommerce_shop_views.xml',
        'views/sale_order_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
}