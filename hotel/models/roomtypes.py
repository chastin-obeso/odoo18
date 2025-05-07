from odoo import models, fields, api

class RoomTypes(models.Model):
    _name = 'hotel.roomtypes'  # Model name
    _description = 'Room Types'

    name = fields.Char("Room Type", required=True)
    description = fields.Char("Room Type Description")
    photobed = fields.Image("Bed Photo")
    photorestroom = fields.Image("Comfort Room Photo")
    dailycharges_ids = fields.One2many('hotel.dailycharges', 'roomtype_id', string='Daily Charges')
    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string='Rooms')
    roomtype_id = fields.Many2one('hotel.roomtypes', string='Room Type', ondelete='cascade')
    
# class HotelRoomTypeCharge(models.Model):
#     _name = 'hotel.roomtype.charge'
#     _description = 'Daily Charge'

#     roomtype_id = fields.Many2one('hotel.roomtypes', string='Room Type', ondelete='cascade')
#     day = fields.Selection([
#         ('mon', 'Monday'),
#         ('tue', 'Tuesday'),
#         ('wed', 'Wednesday'),
#         ('thu', 'Thursday'),
#         ('fri', 'Friday'),
#         ('sat', 'Saturday'),
#         ('sun', 'Sunday'),
#     ], string='Day', required=True)
#     rate = fields.Float(string='Rate', required=True)

class dailycharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'hotel roomtype daily charges list'
    charge_id = fields.Many2one('hotel.charges',string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10,2), options={'always_reload': True})
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Roomtype")