# -*- coding: utf-8 -*-
#----------------------------------------------------------
# ir_http modular http routing
#----------------------------------------------------------
import base64
import hashlib
import logging
import mimetypes
import os
import re
import sys
import traceback

import werkzeug
import werkzeug.exceptions
import werkzeug.routing
import werkzeug.urls
import werkzeug.utils

import odoo
from odoo import api, http, models, tools, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError
from odoo.http import request, content_disposition
from odoo.tools import consteq, pycompat
from odoo.tools.mimetypes import guess_mimetype
from odoo.modules.module import get_resource_path, get_module_path

from odoo.http import ALLOWED_DEBUG_MODES
from odoo.tools.misc import str2bool

_logger = logging.getLogger(__name__)

from odoo.addons.base.models.ir_http import IrHttp

# start modify
def _binary_record_content(self, record, field='datas', filename=None, filename_field='name', default_mimetype='application/octet-stream'):
   model = record._name
   mimetype = 'mimetype' in record and record.mimetype or False
   content = None
   filehash = 'checksum' in record and record['checksum'] or False

   field_def = record._fields[field]
   if field_def.type == 'binary' and field_def.attachment:
      field_attachment = self.env['ir.attachment'].sudo().search_read(domain=[('res_model', '=', model), ('res_id', '=', record.id), ('res_field', '=', field)], fields=['datas', 'mimetype', 'checksum'], limit=1)
      if field_attachment:
            mimetype = field_attachment[0]['mimetype']
            content = field_attachment[0]['datas']
            filehash = field_attachment[0]['checksum']

   if not content:
      content = record[field] or ''

   # filename
   default_filename = False
   if not filename:
      if filename_field in record:
            if model == 'product.supplierinfo':
               filename = record['product_name']
            else:
               filename = record[filename_field]
      if not filename:
            default_filename = True
            filename = "%s-%s-%s" % (record._name, record.id, field)

   if not mimetype:
      try:
            decoded_content = base64.b64decode(content)
      except base64.binascii.Error:  # if we could not decode it, no need to pass it down: it would crash elsewhere...
            return (404, [], None)
      mimetype = guess_mimetype(decoded_content, default=default_mimetype)

   # extension
   _, existing_extension = os.path.splitext(filename)
   if not existing_extension or default_filename:
      extension = mimetypes.guess_extension(mimetype)
      if extension:
            filename = "%s%s" % (filename, extension)

   if not filehash:
      filehash = '"%s"' % hashlib.md5(pycompat.to_text(content).encode('utf-8')).hexdigest()

   status = 200 if content else 404
   return status, content, filename, mimetype, filehash

IrHttp._binary_record_content = _binary_record_content # apply the modify