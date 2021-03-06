import irc3
from ircbot.models import OutgoingIrcMessage
from django.conf import settings
from django.utils import timezone
import logging
logger = logging.getLogger("bornhack.%s" % __name__)


@irc3.plugin
class Plugin(object):
    """BornHack IRC3 class"""

    requires = [
        'irc3.plugins.core', # makes the bot able to connect to an irc server and do basic irc stuff
        'irc3.plugins.userlist', # maintains a convenient list of the channels the bot is in and their users
        'irc3.plugins.command', # what does this do?
    ]

    def __init__(self, bot):
        self.bot = bot


    ###############################################################################################
    ### builtin irc3 event methods

    def server_ready(self, **kwargs):
        """triggered after the server sent the MOTD (require core plugin)"""
        logger.debug("inside server_ready(), kwargs: %s" % kwargs)


    def connection_lost(self, **kwargs):
        """triggered when connection is lost"""
        logger.debug("inside connection_lost(), kwargs: %s" % kwargs)


    def connection_made(self, **kwargs):
        """triggered when connection is up"""
        logger.debug("inside connection_made(), kwargs: %s" % kwargs)

        # wait 5 secs before starting the loop to check for outgoing messages
        self.bot.loop.call_later(settings.IRCBOT_CHECK_MESSAGE_INTERVAL_SECONDS, self.bot.get_outgoing_messages)


    ###############################################################################################
    ### decorated irc3 event methods

    @irc3.event(irc3.rfc.JOIN_PART_QUIT)
    def on_join_part_quit(self, **kwargs):
        """triggered when there is a join part or quit on a channel the bot is in"""
        logger.debug("inside on_join_part_quit(), kwargs: %s" % kwargs)


    @irc3.event(irc3.rfc.PRIVMSG)
    def on_privmsg(self, **kwargs):
        """triggered when a privmsg is sent to the bot or to a channel the bot is in"""
        logger.debug("inside on_privmsg(), kwargs: %s" % kwargs)

        # nickserv
        if kwargs['mask'] == "NickServ!NickServ@services.baconsvin.org" and kwargs['event'] == "NOTICE" and kwargs['data'] == "This nickname is registered. Please choose a different nickname, or identify via \x02/msg NickServ identify <password>\x02.":
            logger.info("Nickserv identify needed, fixing...")
            self.bot.privmsg("NickServ@services.baconsvin.org", "identify %s %s" % (settings.IRCBOT_NICK, settings.IRCBOT_NICKSERV_PASSWORD))


    @irc3.event(irc3.rfc.KICK)
    def on_kick(self, **kwargs):
        logger.debug("inside on_kick(), kwargs: %s" % kwargs)


    ###############################################################################################
    ### custom irc3 methods

    @irc3.extend
    def get_outgoing_messages(self):
        """
            This method gets unprocessed OutgoingIrcMessage objects and attempts to send them to
            the target channel. Messages are skipped if the bot is not in the channel.
        """
        #logger.debug("inside get_outgoing_messages()")
        for msg in OutgoingIrcMessage.objects.filter(processed=False).order_by('created'):
            logger.info("processing irc message to %s: %s" % (msg.target, msg.message))
            # if this message expired mark it as expired and processed without doing anything
            if msg.timeout < timezone.now():
                logger.info("this message is expired, marking it as such instead of sending it to irc")
                msg.expired=True
                msg.processed=True
                msg.save()
                continue

            # is this message for a channel or a nick?
            if msg.target[0] == "#" and msg.target in self.bot.channels:
                logger.info("sending privmsg to %s: %s" % (msg.target, msg.message))
                self.bot.privmsg(msg.target, msg.message)
                msg.processed=True
                msg.save()
            elif msg.target:
                logger.info("sending privmsg to %s: %s" % (msg.target, msg.message))
                self.bot.privmsg(msg.target, msg.message)
                msg.processed=True
                msg.save()
            else:
                logger.warning("skipping message to %s" % msg.target)

        # call this function again in X seconds
        self.bot.loop.call_later(settings.IRCBOT_CHECK_MESSAGE_INTERVAL_SECONDS, self.bot.get_outgoing_messages)


