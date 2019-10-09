# kopano-dagent RewriteGALAddressesToSMTP
# (c) 2017 Hein-Pieter van Braam <hp@tmm.cx>
# Licensed under the GPU Affero GPL v3 (or at your option any later version)
# See LICENSE file for details

import MAPI
import email
from email.utils import getaddresses
from email.header import decode_header

from MAPI.Util import *
from plugintemplates import *

class RewriteGALAddressesToSMTP(IMapiDAgentPlugin):
    
    def __init__(self, logger):
        IMapiDAgentPlugin.__init__(self, logger)

    def DecodeHeaderToUTF8(self, header):
        decodedHeader = decode_header(header)
        headerText, headerEncoding = decodedHeader[0]
        if headerEncoding is None:
            return str(headerText)
        else:
            return str(headerText, headerEncoding, 'ignore')

    def PreDelivery(self, session, addrbook, store, folder, message):
        headers = message.GetProps([PR_TRANSPORT_MESSAGE_HEADERS], 0)[0].Value
        msg = email.message_from_bytes(headers)
        to_addrs = getaddresses(msg.get_all('to', []))
        cc_addrs = getaddresses(msg.get_all('cc', []))
    
        names = []
        for addr in to_addrs:
            names.append([
                SPropValue(PR_RECIPIENT_TYPE, MAPI_TO),
                SPropValue(PR_DISPLAY_NAME_W, self.DecodeHeaderToUTF8(addr[0])),
                SPropValue(PR_ADDRTYPE, 'SMTP'),
                SPropValue(PR_EMAIL_ADDRESS, bytes(addr[1],'utf-8')),
            ])
    
        for addr in cc_addrs:
            names.append([
                SPropValue(PR_RECIPIENT_TYPE, MAPI_CC),
                SPropValue(PR_DISPLAY_NAME_W, self.DecodeHeaderToUTF8(addr[0])),
                SPropValue(PR_ADDRTYPE, 'SMTP'),
                SPropValue(PR_EMAIL_ADDRESS, bytes(addr[1],'utf-8')),
            ])
    
        message.ModifyRecipients(0, names)
        return MP_CONTINUE,

