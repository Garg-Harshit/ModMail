import discord
from discord.ext import commands
from random import randint

class HelpCog(commands.Cog, name="help command"):
	def __init__(self, bot):
		self.bot = bot
  

	@commands.command(name = 'help',
					usage="  :",
					description = "Display the help message.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def help (self, ctx, commandName=None):
		embed = discord.Embed(title=f"__**Help page of {self.bot.user.name}**__", description="", color=randint(0, 0xffffff))
		embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
		for i in self.bot.commands:
			embed.add_field(name=f"**{self.bot.command_prefix}{i} {i.usage}**", value=f"{i.description}", inline=False)
		await ctx.channel.send(embed=embed)

def setup(bot):
	bot.remove_command("help")
	bot.add_cog(HelpCog(bot))