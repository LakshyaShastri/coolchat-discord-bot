import discord
from discord.ext import commands
import sys
import logging
import typing
import pendulum
import random
import feedparser
from bs4 import BeautifulSoup


class MiscCog(commands.Cog, name="Miscellaneous"):

    def __init__(self, bot):
        self.bot = bot
        self.__name__ = __name__
    

    @commands.command(name='albert')
    async def fetch_latest_albert(self, ctx):
        """Retrieves latest Albert post from LiveJournal"""
        url = "https://albert71292.livejournal.com/data/rss"
        raw_feed = feedparser.parse(url)
        latest = raw_feed.entries[0]
        post = latest.description.replace("<br />", "\n").replace("<p />", "\n")
        post = BeautifulSoup(post, "lxml").text
        combo = f"{latest.title} - {pendulum.parse(latest.published, strict=False).format('MMM Do, YYYY')}"

        embed = discord.Embed(
            title = combo,
            colour = 0x101921,
            description = post,
            url = latest.link
        )

        embed.set_thumbnail(url=raw_feed.feed.image.href)

        await ctx.send(content=f"**{raw_feed.feed.title}**", embed=embed)


    @commands.command(name='pick', aliases=['choose', 'random', 'choice'])
    async def pick_something_randomly(self, ctx, *, optional_input: str=None):
        """Command to pick something from user input at random"""

        if not optional_input:
            return await ctx.send("I need something to choose from")
        if "," not in optional_input:
            if " or " in optional_input.lower():
                optional_input = optional_input.split(" or ")
            else:
                optional_input = optional_input.split()
        else:
            optional_input = optional_input.split(",")
        if len(optional_input) == 1:
            return await ctx.send("What do you expect from me?")
        elif len(optional_input) >= 10:
            return await ctx.send("Way too many things to choose from, try thinking for yourself!")
        choice = random.choice(optional_input)
        return await ctx.send("{}".format(self._bold(choice.strip())))

    @commands.command(name='source', aliases=['mysource', 'botsource'])
    async def show_source(self, ctx):
        """Command which shows my source code repository link."""

        embed = discord.Embed(title='My Source Code on GitHub',
                              description='@cottongin maintains me',
                              colour=0xFEFEFE,
                              url="https://github.com/cottongin/coolchat-discord-bot")

        embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/782294?s=460&v=4")
        embed.set_footer(text="https://github.com/cottongin/coolchat-discord-bot")

        await ctx.send(embed=embed)

    @commands.command(name='seen', aliases=['last'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def seen_member(self, ctx,
                              member: typing.Optional[discord.Member] = None):
        """Tries to find the last/most recent message from a user
        e.g. seen @ra
        """

        if not member:
            await ctx.send("I need someone to look for!")
            return

        message = await ctx.send("Hang on, I'm searching this channel's chat history (this takes a second)")
        msg = await ctx.channel.history(limit=None).get(author=member)
        if not msg:
            await message.edit(content="I couldn't find a recent message from {}".format(
                self._mono(member.display_name)
            ))
            return
        await message.edit(content="I last saw {} in here {} saying: \n{}".format(
            self._mono(member.display_name), 
            pendulum.parse(str(msg.created_at), strict=False).diff_for_humans(),
            self._quote(msg.clean_content)))


    def _strikethrough(self, text):
        return "~~{}~~".format(text)

    def _bold(self, text):
        return "**{}**".format(text)

    def _italics(self, text):
        return "*{}*".format(text)

    def _quote(self, text):
        return "> {}".format(text)

    def _mono(self, text):
        return "`{}`".format(text)

    def _code(self, text, lang=""):
        return "```{}\n{}\n```".format(lang, text)

    def _spoiler(self, text):
        return "||{}||".format(text)


def setup(bot):
    bot.add_cog(MiscCog(bot))