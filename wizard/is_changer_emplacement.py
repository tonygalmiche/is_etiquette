# -*- coding: utf-8 -*-

import time
import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc

class is_colis(osv.osv_memory):
    _name = 'is.colis'
    _description = 'Colis'
    _columns = {
        'colis_id': fields.many2one('is.etiquette', 'Numero colis', required=True),
        'quantity': fields.float('Quantite', readonly=True),
        'etiquette_id': fields.many2one('is.changer.emplacement', 'Etiquette'),
    }
    
    def onchange_colis_id(self, cr, uid, ids, colis_id, context=None):
        context = context or {}
        value = {}
        if colis_id:
            colis = self.pool.get('is.etiquette').read(cr, uid, colis_id, ['quantity'], context=context)
        
            value = {
                'quantity': colis['quantity'],
            }
        return {'value': value}
    
is_colis()

class is_changer_emplacement(osv.osv_memory):
    _name = 'is.changer.emplacement'
    _description = "changement d'emplacement de colis"
    _columns = {
        'location_src_id': fields.many2one('stock.location', 'Emplacement source', required=True),
        'location_dest_id': fields.many2one('stock.location', 'Emplacement destination', required=True),
        'colis_line': fields.one2many('is.colis', 'etiquette_id', "Colis", required=True),
    }    
    
    def changer_emplacements(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('stock.move')
        etiquette_obj = self.pool.get('is.etiquette')
        colis_obj = self.pool.get('is.colis')
        obj_model = self.pool.get('ir.model.data')
        
        result = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]

        if data:
            for colis_id in data['colis_line']:
                etiquette = colis_obj.read(cr, uid, colis_id, ['colis_id'], context=context)
                colis = etiquette_obj.browse(cr, uid, etiquette['colis_id'][0], context=context)

                value = move_obj.onchange_product_id(cr, uid, ids, colis.prodlot_id.product_id.id, False, False, False)['value']
                vals = {
                    'name': colis.prodlot_id.product_id.name,
                    'product_id': colis.prodlot_id.product_id.id,
                    'product_qty': colis.quantity,
                    'location_id': data['location_src_id'][0],
                    'location_dest_id': data['location_dest_id'][0],
                    'date_expected': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'prodlot_id': colis.prodlot_id.id,
                    'type': 'internal',
                }
                value.update(vals)
                                
                newid = move_obj.create(cr, uid, value, context=context)
                result.append(newid)
        
        action_model = False
        action = {}
        action_model,action_id = obj_model.get_object_reference(cr, uid, 'stock', "action_move_form2")
        
        if action_model:
            action_pool = self.pool.get(action_model)
            action = action_pool.read(cr, uid, action_id, context=context)
            action['domain'] = "[('id','in', ["+','.join(map(str,result))+"])]"
        return action
            
is_changer_emplacement()