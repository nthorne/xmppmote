xmppmote
========

Daemon for remote server administration over XMPP (e.g. control a headless server via Google Chat
on your smart phone).

dependencies
------------

XMPPMote depends on the excellent xmpppy library (http://xmpppy.sourceforge.net/),
and since fancy XMPPMote installers are on the backlog, so you will need to install
that one separately, e.g.

`$ sudo apt-get install python-pyxmpp`

usage
-----

First off, you will need to create a XMPP user ( **use a unique password since the password**
**currently is stored in plain text** ) on e.g. the Jabber network (http://www.jabber.org/create-an-account/),
and then initialise a chat session between that user, and the user that you wish to control
your box with; and since that session initialisation is not yet implemented in XMPPMote,
just go ahead and use a web based jabber client such as JWChat (http://jwchat.org/).

After having set up the XMPP user, run the XMPPMote installation script, e.g.:

`$ sudo ./install.sh /opt/xmppmote`

This will copy the XMPPMote source files to /opt/xmppmote, create a default configuration file
(/opt/xmppmote/xmppmoterc in this example), and copy the XMPPMote init script, and its
configuration file to /etc/init.d and /etc/default, respectively. After having installed
XMPPMote, it is **imperative** that you _start it manually once in order to enter your
credentials_, i.e.

    $ cd /opt/xmppmote
    $ sudo ./xmppmoted.py start

this should cause you to be prompted for the username (including e.g. @jabber.org), and password
that you created for XMPPMote. After having entered the credentials, the bot should be online
in your chat client, and you can chat away with it until your heart is content; at which point
you can type **bye** into your client to terminate the bot.

For more command line options, type

`$ ./xmppmoted.py -h`

In order to have the daemon starting at system startup on an Ubuntu system, use update-rc.d, e.g.:

`$ sudo update-rc.d xmppmote defaults`

On any other system that supports System V style init scripts, you should be able to get the
daemon started automaticall by symlinking the init script to the appropriate runlevels, e.g.

    $ runlevel
    N 2
    $ ln -s /etc/init.d/xmppmote /etc/rc2.d/S99xmppmote

For details regarding the configuration of XMPPMote, please refer to xmppmoterc.example in the
XMPPMote installation directory.

here be dragons
---------------

Please note that this is an early beta software. That, in combination with messing around with
init scripts, can cause some serious problems with your system in case of malconfiguration, so
make sure to verify the XMPPMote installation properly.
