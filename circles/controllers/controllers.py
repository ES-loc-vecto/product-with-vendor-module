# -*- coding: utf-8 -*-
# from odoo import http


# class Circles(http.Controller):
#     @http.route('/circles/circles/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/circles/circles/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('circles.listing', {
#             'root': '/circles/circles',
#             'objects': http.request.env['circles.circles'].search([]),
#         })

#     @http.route('/circles/circles/objects/<model("circles.circles"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('circles.object', {
#             'object': obj
#         })

import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):

    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, token, report_name, **kw):
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
