# from odoo import http


# class CrmJobLeads(http.Controller):
#     @http.route('/crm_job_leads/crm_job_leads', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_job_leads/crm_job_leads/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_job_leads.listing', {
#             'root': '/crm_job_leads/crm_job_leads',
#             'objects': http.request.env['crm_job_leads.crm_job_leads'].search([]),
#         })

#     @http.route('/crm_job_leads/crm_job_leads/objects/<model("crm_job_leads.crm_job_leads"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_job_leads.object', {
#             'object': obj
#         })

