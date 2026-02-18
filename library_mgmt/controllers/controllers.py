# from odoo import http


# class LibraryMgmt(http.Controller):
#     @http.route('/library_mgmt/library_mgmt', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_mgmt/library_mgmt/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_mgmt.listing', {
#             'root': '/library_mgmt/library_mgmt',
#             'objects': http.request.env['library_mgmt.library_mgmt'].search([]),
#         })

#     @http.route('/library_mgmt/library_mgmt/objects/<model("library_mgmt.library_mgmt"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_mgmt.object', {
#             'object': obj
#         })

