# -*- encoding: utf-8 -*-
# © 2017 Fábio Luna, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import requests
import json
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    driver = fields.Char(string="Motorista")
    board = fields.Char(string="Placa")

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        url = ""
        headers = {
            'Content-Type': 'application/json',
            'apikey': ''}
        date = datetime.now()
        date = date.isoformat()

        for item in self:
            if self.get_external_id() != "stock.delivery":
                continue

            vals = dict(
                order_id=self.origin,
                date=date,
                shippingCompany=dict(
                    driver=self.driver,
                    board=self.board,
                ),)

            products = []
            for product in self.move_lines:
                item_vals = dict(
                    id=product.product_id.default_code,
                    quantity=product.quantity_done,
                    volume=self.number_of_packages,
                )

                products.append(item_vals)

            vals.update({'products': products})

            post = json.dumps(vals)
            requests.post(url=url, data=post, headers=headers)

        return res
