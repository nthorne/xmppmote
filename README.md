xmppmote
========

Remote server administration via XMPP (e.g. control a headless server via Google Chat
on your smart phone).

dependencies
------------

XMPPMote depends on the excellent xmpppy library (http://xmpppy.sourceforge.net/),
and since fancy XMPPMote installers are on the backlog, so you will need to install
that one separately, e.g.

`$ sudo apt-get install python-pyxmpp`

usage
-----

First off, you will need to create a XMPP user on e.g. the Jabber network
(http://www.jabber.org/create-an-account/), and then initialise a chat session between
that user, and the user that you wish to control your box with, and since that
session initialisation is not yet implemented in XMPPMote, just go ahead and use
a web based jabber client such as JWChat (http://jwchat.org/).

After having set up the XMPP user, modify configuration/commands.pu to suit your likings
(i.e. command handler type, and possibly a set of allowed commands, if RestrictedCommandHandler
is to be used; if no changes are made, the UnsafeCommandHandler is used, which will basically
throw any incoming command at the shell, hoping that it sticks). After configurating XMPPMote,
it is invoked by typing

`$ ./xmppmote.py <user> <password>`

After having done this, the bot should be online in your chat client, and you can chat away
with it until your heart is content; at which point you can type **bye** into your client to
terminate the bot.

final notes
-----------

This software is in early beta, so don't expect much regarding documentation and user friendliness;
also, important features such as a sane configuration system, daemonization and logging is not
yet in place either.

