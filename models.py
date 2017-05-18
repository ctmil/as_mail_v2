# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate

#Get the logger
_logger = logging.getLogger(__name__)

class as_mail_message(models.Model):
        _inherit = 'as.mail.message'
	_order = 'id desc'

	@api.one
	def _compute_mail_type(self):
		if 'uid' in self.env.context:
			uid = self.env.context['uid']
			user = self.env['res.users'].browse(uid)
			if self.author_id.id == user.partner_id.id:
				self.mail_type = 'outgoing'
			else:
				self.mail_type = 'incoming'
		else:
			self.mail_type = 'unknown'

	@api.one
	def _compute_po_id(self):
		if self.model == 'purchase.order':
			self.po_id = self.res_id

	@api.one
	def _compute_request_id(self):
		if self.model == 'purchase.request':
			self.request_id = self.res_id

	mail_type = fields.Selection(selection=[('incoming','Entrante'),('outgoing','Saliente'),('unknown','Desconocido')],compute=_compute_mail_type)
	po_id = fields.Many2one('purchase.order','Orden de Compra',compute=_compute_po_id)
	request_id = fields.Many2one('purchase.request','Requisicion',compute=_compute_request_id)
