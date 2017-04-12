# kopano-dagent RewriteGALAddressesToSMTP

## What is it

This is a plugin for Kopano (and perhaps Zarafa) dagent that rewrites incoming addresses to the 'SMTP' type.

By default dagent will look up the incoming address (To: and CC:) in the server's GAL and replace the recipients with a ZARAFA:<address> type.
What this means is that the information about what alias was used to receive the message is lost when viewing the message in WebApp or via z-push.

This plugin will read all relevant headers and undo this step.

## Installation

In a default kopano installation the Python plugin path is set to /var/lib/kopano/dagent/plugins. Simply place rewriteusers.py in this directory and restart dagent. No configuration is necessary or possible.

## Requirements

This plugin has been tested on Kopano 8.4.0~254-49, it relies on python email package which should be installed by default.
