# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _


class is_etiquette(osv.osv):
    _name = 'is.etiquette'
    _description = 'gestion des colis'
    
    def _check_quantity(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if data.quantity <= 0:
                return False
        return True
    
    _columns = {
        'name': fields.char('Numero du colis', size=64, required=True, readonly=True),
        'prodlot_id': fields.many2one('stock.production.lot', 'Numero de serie', required=True),
        'quantity': fields.float('Quantite', required=True),
        'location_id': fields.many2one('stock.location', 'Emplacement colis', required=True),
    }
    
    _defaults = {
        'name': ' ',
    }
    
    _constraints = [(_check_quantity, 'Erreur: La quantite doit etre superieure a zero', ['quantity'])]
    
    
    def onchange_prodlot_id(self, cr, uid, ids, prodlot_id, context=None):
        context = context or {}
        value = {}
        if prodlot_id:
            prodlot = self.pool.get('stock.production.lot').read(cr, uid, prodlot_id, ['product_id'], context=context)
            
            pack_ids = self.pool.get('product.packaging').search(cr, uid, [('product_id','=',prodlot['product_id'][0]),], context=context)
            quantity = 0
            if pack_ids:
                pack = self.pool.get('product.packaging').read(cr, uid, pack_ids[0], ['qty'], context=context)
                quantity = pack['qty']
        
            value = {
                'quantity': quantity,
            }
        return {'value': value}
    
    
    def create(self, cr, uid, vals, context=None):
        data_obj = self.pool.get('ir.model.data')
        sequence_ids = data_obj.search(cr, uid, [('name','=','seq_is_etiquette')], context=context) 
        if vals.get('name',' ') ==' ':
            sequence_id = data_obj.browse(cr, uid, sequence_ids[0], context=context).res_id
            code = self.pool.get('ir.sequence').get_id(cr, uid, sequence_id, 'id', context) or ' '
            vals['name'] = code
         
        return super(is_etiquette, self).create(cr, uid, vals, context=context)
    
is_etiquette()   
