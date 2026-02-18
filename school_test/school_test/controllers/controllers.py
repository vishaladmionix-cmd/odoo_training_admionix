# from odoo import http


# class SchoolTest(http.Controller):
#     @http.route('/school_test/school_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_test/school_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_test.listing', {
#             'root': '/school_test/school_test',
#             'objects': http.request.env['school_test.school_test'].search([]),
#         })

#     @http.route('/school_test/school_test/objects/<model("school_test.school_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_test.object', {
#             'object': obj
#         })

