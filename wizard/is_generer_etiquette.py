# -*- coding: utf-8 -*-

import time
import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc

class is_generer_etiquette(osv.osv_memory):
    _name = 'is.generer.etiquette'
    _description = "Generer les etiquettes"
    
    def _check_nb_colis(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if data.nb_colis == 0:
                return False
        return True
    
    _columns = {
        'prodlot_id': fields.many2one('stock.production.lot', 'Numero de serie', required=True),
        'quantity': fields.float('Quantite', readonly=True),
        'location_id': fields.many2one('stock.location', 'Emplacement colis', required=True),
        'nb_colis': fields.integer('Nombre de colis'),
    }
    
    _constraints = [(_check_nb_colis, 'Erreur: Le nombre de colis doit etre superieure a zero', ['nb_colis'])]
    
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
    
    def get_quantity(self, cr, uid, prodlot_id, context=None):
        if prodlot_id:
            prodlot = self.pool.get('stock.production.lot').read(cr, uid, prodlot_id, ['product_id'], context=context)
            product_id = prodlot['product_id'][0]
            
            pack_ids = self.pool.get('product.packaging').search(cr, uid, [('product_id','=',product_id),], context=context)
            if pack_ids:
                pack = self.pool.get('product.packaging').read(cr, uid, pack_ids[0], ['qty'], context=context)
                return pack['qty']
            else:
                return 0
                
    
    
    def generer_etiquettes(self,cr, uid, ids, context=None):
        etiquette_obj = self.pool.get('is.etiquette')
        obj_model = self.pool.get('ir.model.data')
        
        result = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]

        if data:
            i = 1
            qty = self.get_quantity(cr, uid, data['prodlot_id'][0], context=context)
            if qty:
                while i <= data['nb_colis'] :                
                    vals = {
                        'prodlot_id': data['prodlot_id'][0],
                        'quantity': qty,
                        'location_id': data['location_id'][0],
                        }
                    newid = etiquette_obj.create(cr, uid, vals, context=context)
                    result.append(newid)
                    i += 1
                
                action_model = False
                action = {}
                action_model,action_id = obj_model.get_object_reference(cr, uid, 'is_etiquette', "action_is_etiquette_form")
        
                if action_model:
                    action_pool = self.pool.get(action_model)
                    action = action_pool.read(cr, uid, action_id, context=context)
                    action['domain'] = "[('id','in', ["+','.join(map(str,result))+"])]"
                return action
            else:
                model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),('name','=','is_quantity_null_view')])
                resource_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
                return {
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'is.import.contract',
                        'views': [(resource_id,'form')],
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'context': context,
                }
    
    
is_generer_etiquette()
