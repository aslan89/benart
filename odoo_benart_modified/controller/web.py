# -*- coding: utf-8 -*-
import base64
from odoo import http, _
from odoo.http import request
import werkzeug
from odoo.addons.web.controllers import main

values = {
    'certificate_number': _('Certificate Number'),
    'firm_name': _('Firm Name')
}


class Web(http.Controller):

    @http.route('/get_search_certificate', auth='public', website=True)
    def get_search_certificate(self, **kw):
        return http.request.render('odoo_benart_modified.search_certificate',
                                   {'certificate_number': '', 'firm_name': ''})

    @http.route('/post_search_certificate', auth='public', website=True)
    def post_search_certificate(self, **kw):
        required = ['certificate_number', 'firm_name']
        errors = []
        for i in required:
            if i not in kw.keys():
                errors.append(_('{} required.'.format(values[i])))
        # try:
        #     validate = request.env['website.form.recaptcha'].sudo().validate_request(request, kw)
        #     if not validate:
        #         errors.append(_("Recaptcha validate!"))
        # except:
        #     errors.append(_("Recaptcha validate!"))

        if errors:
            return http.request.render('odoo_benart_modified.search_certificate',
                                       {
                                           'errors': errors,
                                           'certificate_number': kw.get('certificate_number', ''),
                                           'firm_name': kw.get('firm_name', '')
                                       })

        records = request.env['benart.certificate'].sudo().search(
            [('certification_number', '=', kw['certificate_number']),
             ('res_partner_id.name', 'ilike', kw['firm_name']),
             ('certificate_status', '=', 'active')])

        certificate_search_text = request.env['benart.parameter'].sudo().search([
            ('parameter_name', '=', 'certificate_search_text')
        ], limit=1)

        return http.request.render('odoo_benart_modified.search_certificate',
                                   {
                                       'records': records,
                                       'certificate_search_text': certificate_search_text,
                                       'errors': errors,
                                       'certificate_number': kw.get('certificate_number', ''),
                                       'firm_name': kw.get('firm_name', '')
                                   })

    @http.route('/documents', auth='public', website=True)
    def documents(self, **kw):
        domain = [('parameter_name', '=', 'document_type')]
        if 'type' in kw.keys() and self.represents_int(kw.get("type", "all")):
            domain.append(('document_type_id', '=', int(kw.get('type', 0))))
        documents = request.env['benart.parameter'].sudo().search(domain)
        document_types = request.env['benart.document_type'].sudo().search([])
        return http.request.render('odoo_benart_modified.documents',
                                   {'documents': documents, 'document_types': document_types,
                                    'selected_type': str(kw.get("type", 'all'))})

    @staticmethod
    def represents_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @http.route('/download/document/<int:id>', type='http', auth="public")
    def download_document(self, id=None, **kw):
        status, headers, content = main.binary_content(
            xmlid=None, model='benart.parameter', id=id, field='file', unique=None, filename=None,
            filename_field='file_name', download=True, mimetype=None,
            access_token=None, related_id=None, access_mode=None)
        if status == 304:
            response = werkzeug.wrappers.Response(status=status, headers=headers)
        elif status == 301:
            return werkzeug.utils.redirect(content, code=301)
        elif status != 200:
            response = request.not_found()
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        return response
