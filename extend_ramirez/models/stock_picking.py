
from odoo import _, api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    qty_product = fields.Integer(
        string='Cantidad',
        compute="_compute_qty_product"
    )

    @api.depends('move_ids_without_package.quantity_done')
    def _compute_qty_product(self):
        for rec in self:
            if rec.move_ids_without_package:
                for l in rec.move_ids_without_package:
                    if l.quantity_done:
                        rec.qty_product += l.quantity_done
                    else:
                        rec.qty_product += 0
            else:
                rec.qty_product += 0


    cost = fields.Float(
        string='$',
        compute="_compute_cost"
    )

    @api.depends('picking_type_id','move_ids_without_package.quantity_done')
    def _compute_cost(self):
        for rec in self:
            if rec.picking_type_id.code == 'incoming':
                amount = 0
                for l in rec.move_ids_without_package:
                    print("-------------")
                    if l.product_id:
                        for p in l.product_id.seller_ids:
                            print("-------------",p.name.id,l.partner_id.id)
                            if p.name.id == rec.partner_id.id:
                                print("-------------")
                                amount += p.price * l.quantity_done
                rec.cost = amount
            elif rec.picking_type_id.code == 'outgoing':
                amount = 0
                for l in rec.move_ids_without_package:
                    if l.product_id.lst_price > 0 and l.quantity_done > 0:
                        amount += l.product_id.lst_price * l.quantity_done
                rec.cost = amount

            elif rec.picking_type_id.code == 'internal':
                amount = 0
                for l in rec.move_ids_without_package:
                    if l.product_id.lst_price > 0 and l.quantity_done > 0:
                        amount += l.product_id.lst_price * l.quantity_done
                rec.cost = amount

            else:
                rec.cost = 0.0





