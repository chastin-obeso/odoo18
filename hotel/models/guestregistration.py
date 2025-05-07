#Guest Registration Model

# -*- coding: utf-8 -*-

#guestregistration.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'hotel guest registration list'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")

    #roomname -< related fields found in the model hotel.rooms    
    roomname=fields.Char("Room No.",related='room_id.name')

    #roomtname <- room type name found in the model hotel.rooms 
    # also related to hotel.roomtypes
    roomtname=fields.Char("Room Type",related='room_id.name')

    #guestname <- related field found as a computed field called name in 
    #the model hotel.guests
    guestname=fields.Char("Guest Name",related='guest_id.name')
    datecreated = fields.Date("Date Created", default=lambda self: fields.Date.today())
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")
    #computed field called name <- concatenation of room name and guest name
    name= fields.Char("Guest Registration",compute='_compute_name',store=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', readonly=True)

    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for rec in self:
            room = rec.room_id.name or ''
            guest_first = rec.guest_id.firstname or ''
            guest_last = rec.guest_id.lastname or ''
            guest = f"{guest_first} {guest_last}".strip()
            rec.name = f"{room}, {guest}" if room or guest else ''

    def action_reserve(self):
        for rec in self:
            if not(rec.guest_id):  
                raise ValidationError('Please supply a valid guest.')            
           
            elif not(rec.roomname):    
                raise ValidationError('Please supply a valid Room Number.')            
            else:
                pkid = rec.id
                self._cr.execute("select * from public.fncheck_registrationconflict("+str(pkid)+")")
                result = self._cr.fetchall()
               
                result_cnt = result[0][0]
                result_msg = result[0][1]
               
                if (result_cnt==0):
                    rec.state= "reserved"
                else:
                    raise ValidationError(result_msg)
                               
    def action_checkin(self):
        for rec in self:
            if not(rec.guest_id):  
                raise ValidationError('Please supply a valid guest.')            
           
            elif not(rec.roomname):    
                raise ValidationError('Please supply a valid Room Number.')            
            else:
                pkid = rec.id
                self._cr.execute("select * from public.fncheck_registrationconflict("+str(pkid)+")")
                result = self._cr.fetchall()
               
                result_cnt = result[0][0]
                result_msg = result[0][1]
               
                if (result_cnt==0):
                    rec.state= "checked_in"
                else:
                    raise ValidationError(result_msg)
         
    def action_checkout(self):
       for rec in self:
         if (rec.state=="checked_in"):  
            rec.state= "checked_out"
         else:                    
            raise ValidationError("Guest is not CHECKED IN.")

    def action_cancel(self):
       for rec in self:
         if (rec.state=="checked_in"):  
            raise ValidationError("Guest has already CHECKED IN.")          
         else:                    
            rec.state= "cancelled"

