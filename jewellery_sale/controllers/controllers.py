# from odoo import http


# class JewellerySale(http.Controller):
#     @http.route('/jewellery_sale/jewellery_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jewellery_sale/jewellery_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jewellery_sale.listing', {
#             'root': '/jewellery_sale/jewellery_sale',
#             'objects': http.request.env['jewellery_sale.jewellery_sale'].search([]),
#         })

#     @http.route('/jewellery_sale/jewellery_sale/objects/<model("jewellery_sale.jewellery_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jewellery_sale.object', {
#             'object': obj
#         })

