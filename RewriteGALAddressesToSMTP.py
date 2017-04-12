# kopano-dagent RewriteGALAddressesToSMTP
# (c) 2017 Hein-Pieter van Braam <hp@tmm.cx>
# Licensed under the GPU Affero General Public License v3
# See LICENSE file for details

import MAPI
import email
from email.utils import getaddresses

from MAPI.Util import *
from plugintemplates import *

class RewriteGALAddressesToSMTP(IMapiDAgentPlugin):
    
    def __init__(self, logger):
        IMapiDAgentPlugin.__init__(self, logger)

    def PreDelivery(self, session, addrbook, store, folder, message):
        headers = message.GetProps([PR_TRANSPORT_MESSAGE_HEADERS], 0)[0].Value
        msg = email.message_from_string(headers)
        to_addrs = getaddresses(msg.get_all('to', []))
        cc_addrs = getaddresses(msg.get_all('cc', []))
    
        names = []
        for addr in to_addrs:
            names.append([
                SPropValue(PR_RECIPIENT_TYPE, MAPI_TO),
                SPropValue(PR_DISPLAY_NAME_W, unicode(addr[0])),
                SPropValue(PR_ADDRTYPE, 'SMTP'),
                SPropValue(PR_EMAIL_ADDRESS, unicode(addr[1])),
            ])
    
        for addr in cc_addrs:
            names.append([
                SPropValue(PR_RECIPIENT_TYPE, MAPI_CC),
                SPropValue(PR_DISPLAY_NAME_W, unicode(addr[0])),
                SPropValue(PR_ADDRTYPE, 'SMTP'),
                SPropValue(PR_EMAIL_ADDRESS, unicode(addr[1])),
            ])
    
        message.ModifyRecipients(0, names)
        return MP_CONTINUE,

