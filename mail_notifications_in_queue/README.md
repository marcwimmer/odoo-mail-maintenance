#1 mail_notifications_in_queue

If mailserver is unstable then notifications get lost, because they are not 
resent. This module turns force_send to False.
By this of course other mails get lost, if the transaction crashes.

#2 Contributors

* Marc Wimmer <marc@itewimmer.de>

