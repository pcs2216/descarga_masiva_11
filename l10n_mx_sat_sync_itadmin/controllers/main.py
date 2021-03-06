# -*- coding: utf-8 -*-

from odoo.addons.web.controllers.main import Action
from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
#Set company_id variable, so it is accessible in Action domain

class ActionSatSync(Action):
    _description = 'ActionSatSync' 


    @http.route()
    def load(self, action_id, additional_context=None):
        value = super(ActionSatSync, self).load(action_id, additional_context)
        if value and value.get('xml_id','')=='l10n_mx_sat_sync_itadmin.action_attachment_cfdi_supplier_invoices':
            user = request.env.user
            ctx = {}
            try:
                ctx = value.get('context','{}')
                ctx = eval(ctx)
                if 'company_id' not in ctx:
                    ctx.update({'company_id':user.company_id.id})
                    value['context']=str(ctx)
            except Exception:
                pass
            
            #Payroll manager can see only Tipo de comprobante = Nominas de empleados
#            if not user.has_group('hr_payroll.group_hr_payroll_manager'):
#                try:
#                    domain = value.get('domain','[]')
#                    if 'cfdi_type' not in domain:
#                        domain = safe_eval(domain, ctx)
#                        domain.append(('cfdi_type','!=','N'))
#                        value['domain']=domain
#                except Exception:
#                    pass
                
        return value
