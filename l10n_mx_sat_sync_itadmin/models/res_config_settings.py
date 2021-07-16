# -*- coding: utf-8 -*-

from odoo import models, api, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    l10n_mx_esignature_ids = fields.Many2many(related='company_id.l10n_mx_esignature_ids', 
        string='MX E-signature', readonly=False)
    last_cfdi_fetch_date = fields.Datetime("Last CFDI fetch date", related="company_id.last_cfdi_fetch_date", readonly=False)
    default_product_type = fields.Selection(selection='_selection_product_type', string='Crear Productos', required=True,
        help='A stockable product is a product for which you manage stock. The "Inventory" app has to be installed.\n'
             'A consumable product, on the other hand, is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.\n'
             'A digital content is a non-material product you sell online. The files attached to the products are the one that are sold on '
             'the e-commerce such as e-books, music, pictures,... The "Digital Product" module has to be installed.')
    si_producto_no_tiene_codigo = fields.Selection([('Crear automatico', 'Crear automatico'),('Buscar manual', 'Usar producto por defecto')], 'Si producto no se encuentra')
    buscar_producto_por_clave_sat = fields.Boolean("Buscar producto por clave SAT")
    
    @api.model
    def _selection_product_type(self):
        product_obj = self.env['product.product']
        return product_obj._fields.get('type')._description_selection(product_obj.env)
        
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        param_obj = self.env['ir.config_parameter'].sudo()
        res.update(
            default_product_type=param_obj.get_param('l10n_mx_sat_sync_itadmin.default_product_type'),
            si_producto_no_tiene_codigo=param_obj.get_param('l10n_mx_sat_sync_itadmin.si_producto_no_tiene_codigo'),
            buscar_producto_por_clave_sat=param_obj.get_param('l10n_mx_sat_sync_itadmin.buscar_producto_por_clave_sat')
        )
        return res

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param_obj = self.env['ir.config_parameter'].sudo()
        param_obj.set_param('l10n_mx_sat_sync_itadmin.default_product_type', self.default_product_type)
        param_obj.set_param('l10n_mx_sat_sync_itadmin.si_producto_no_tiene_codigo', self.si_producto_no_tiene_codigo)
        param_obj.set_param('l10n_mx_sat_sync_itadmin.buscar_producto_por_clave_sat', self.buscar_producto_por_clave_sat)
        return res
    
    @api.multi
    def import_sat_invoice(self):
        self.company_id.download_cfdi_invoices()
        return True