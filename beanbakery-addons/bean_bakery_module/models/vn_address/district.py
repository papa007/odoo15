from odoo import models, fields
from odoo.tools.translate import translate

class District(models.Model):
    # _name is the important field to define the global name of model
    _name = "res.country.district"
    # _descriptin is define the friendly name for model
    _description = "District"
    _order = "code"
    
    code = fields.Char(string="District Code",help='The District code.', required=True)
    slug = fields.Char(string="District Code ID")
    city_id = fields.Many2one(comodel_name='res.country.city',string='parent_city')
    name = fields.Char('District name', translate=True)
   
    