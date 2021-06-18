import discord
from discord import embeds
from discord import message
from discord import channel
from discord.ext import commands,tasks
import json
from discord.utils import get

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	host_server=data.get("host_server",None)
	client_server=data.get("client_server",None)
	owners_bot = data.get("owners",[])


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents 
intents = discord.Intents.all()

bot = commands.Bot(prefix, intents = intents)

# Load cogs
initial_extensions = [
	"Cogs.onCommandError",
	"Cogs.help",
	"Cogs.ping"
]

print(initial_extensions)

if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(f"Failed to load extension {extension}")


def check_admin_owner(ctx):
	return ctx.message.author.guild_permissions.administrator or ctx.author.id in owners_bot or ctx.author==ctx.guild.owner
@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	await bot.change_presence(status=discord.Status.idle ,activity=discord.Activity(type=discord.ActivityType.listening, name =f"DM reports!"))
	print(discord.__version__)
	send_json_backup.start()


@bot.command(description = "Used to Set-UP Mod Mail." , usage="   :")
@commands.check(check_admin_owner)
async def setup(ctx):
	def author_check(msg):
		return msg.author == ctx.author and msg.channel == ctx.channel
	while True:
		with open("configuration.json", "r") as config: 
			server_json = json.load(config)
		await ctx.send(embed = discord.Embed(title = 'SERVER' , description = 'Would You Like to Keep Seperate Server For Recieving DM\'s? \n1) Enter `Yes` to Keep Seperate Server for Recieving DM\'s \n2) Enter `No` if You Would Like to Keep Same Server.\n3) Enter `cancel` to cancel this setup.' , color=0xff5733 ) )
		choice = await bot.wait_for( "message" , check = author_check )
		if choice.content in [ "YES" , "Yes" , "yes" , "y" , "Y" ]:
			try:
				server_json["host_server"]=int(ctx.guild.id)
				await ctx.send(embed=discord.Embed(title="Server Id" , description = "Enter Server Id of Recieving Server.", color=0xff5733 ))
				message = await bot.wait_for( "message" , check = author_check )
				server_json["client_server"]=int(message.content)
				while(not get(bot.guilds,id=server_json["client_server"])):
					await ctx.send(embed = discord.Embed(title = "Guild ID Invalid",description=f"Please Enter a Valid Server ID or Invite This Bot There Also using given link - \n https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot"))
					message = await bot.wait_for( "message" , check = author_check )
					server_json["client_server"]=int(message.content)
				server_json['Open DM']=((await (get(bot.guilds,id=server_json["client_server"])).create_category("Open DM\'s",overwrites ={ (get(bot.guilds,id=server_json["client_server"])).default_role: discord.PermissionOverwrite(view_channel=False,connect=False)})).id)
				server_json['Closed DM']=((await (get(bot.guilds,id=server_json["client_server"])).create_category("Closed DM\'s",overwrites ={ (get(bot.guilds,id=server_json["client_server"])).default_role: discord.PermissionOverwrite(view_channel=False,connect=False)})).id)
				await ctx.send(embed = discord.Embed(title = 'Message' , description = 'What Message You would Like to Post When a User Posts A Query ? ' , color=0xff5733 ) )
				server_json['DM Welcome Message'] = (await bot.wait_for( "message" , check = author_check )).content
				await ctx.send(embed = discord.Embed(title = 'Message' , description = 'What Message You would Like to Post When a You Close A Query ? ' , color=0xff5733 ) )
				server_json['DM By Message'] = (await bot.wait_for( "message" , check = author_check )).content
				server_json['Backup JSON']=((await (get(bot.guilds,id=server_json["client_server"])).create_text_channel("ModMail Backup JSON",overwrites ={ (get(bot.guilds,id=server_json["client_server"])).default_role: discord.PermissionOverwrite(view_channel=False,connect=False)})).id)
				await ctx.send(embed = discord.Embed(title = "Setup Completed" , description = "All Setup Is Compleated i.e, 2 Catagories are Created Named `Open DM\'s` and `Closed DM\'s` in Recieving Server \n`Open DM\'s` Will Contain Channels that have Qngoing Query i.e, Ticket is Open. \n `Closed DM\'s` will contain Channels whose Query is Cleared i.e, Ticket is Closed.\nAnd also A channel is created which will contain backup of JSON file." , color = 0x1900FF ))
			except:
				await ctx.send(embed = discord.Embed( title = ":x: Error" , description = "You Entered Some Thing Wrong. Please Try Again!" , color = 0xFF0000 ) )
		elif choice.content in [ "No" , "no" , "NO" , "n" , "N" , "nO"]:
			try:
				server_json["host_server"]=int(ctx.guild.id)
				server_json["client_server"]=int(ctx.guild.id)
				server_json['Open DM']=((await (get(bot.guilds,id=server_json["client_server"])).create_category("Open DM\'s",overwrites ={ (get(bot.guilds,id=server_json["client_server"])).default_role: discord.PermissionOverwrite(view_channel=False,connect=False)})).id)
				server_json['Closed DM']=((await (get(bot.guilds,id=server_json["client_server"])).create_category("Closed DM\'s",overwrites ={ (get(bot.guilds,id=server_json["client_server"])).default_role: discord.PermissionOverwrite(view_channel=False,connect=False)})).id)
				await ctx.send(embed = discord.Embed(title = 'Message' , description = 'What Message You would Like to Post When a User Posts A Query ? ' , color=0xff5733 ) )
				server_json['DM Welcome Message'] = (await bot.wait_for( "message" , check = author_check )).content
				await ctx.send(embed = discord.Embed(title = 'Message' , description = 'What Message You would Like to Post When a You Close A Query ? ' , color=0xff5733 ) )
				server_json['DM By Message'] = (await bot.wait_for( "message" , check = author_check )).content
				server_json['Backup JSON']=((await (get(bot.guilds,id=server_json["client_server"])).create_text_channel("ModMail Backup JSON",overwrites ={ (get(bot.guilds,id=server_json["client_server"])).default_role: discord.PermissionOverwrite(view_channel=False,connect=False)})).id)
				await ctx.send(embed = discord.Embed(title = "Setup Completed" , description = "All Setup Is Compleated i.e, 2 Catagories are Created Named `Open DM\'s` and `Closed DM\'s` \n`Open DM\'s` Will Contain Channels that have Qngoing Query i.e, Ticket is Open. \n `Closed DM\'s` will contain Channels whose Query is Cleared i.e, Ticket is Closed.\nAnd also A channel is created which will contain backup of JSON file." , color = 0x1900FF ))
			except:
				await ctx.send(embed = discord.Embed( title = ":x: Error" , description = "You Entered Some Thing Wrong. Please Try Again!" , color = 0xFF0000 ) )
		elif choice.content == "cancel":
			await ctx.send( embed = discord.Embed( title = "Process Cancelled" ) )
		else:
			await ctx.send(embed = discord.Embed( title = ":x: Error" , description = "You Entered an Wrong Choice. Please Try Again!" , color = 0xFF0000 ) )
			continue
		with open('configuration.json','w') as json_file_open:
			json.dump(server_json,json_file_open,indent=4)
			json_file_open.close()
		break


@bot.command(description = "Used to Change Message to send When Ticket is Opened.",usage="   :")
async def open_msg(ctx):
	def author_check(msg):
		return msg.author == ctx.author and msg.channel == ctx.channel
	with open("configuration.json", "r") as config: 
		server_json = json.load(config)
	try:
		await ctx.send(embed = discord.Embed(title = 'Message' , description = 'What Message You would Like to Post When a User Posts A Query ? ' , color=0xff5733 ) )
		server_json['DM Welcome Message'] = (await bot.wait_for( "message" , check = author_check )).content
		await ctx.send(embed= discord.Embed(title="Sucessfully Changed!"))
	except:
		await ctx.send(embed = discord.Embed( title = ":x: Error" , description = "You Entered Some Thing Wrong. Please Try Again!" , color = 0xFF0000 ) )
	with open('configuration.json','w') as json_file_open:
		json.dump(server_json,json_file_open,indent=4)
		json_file_open.close()


@bot.command(description = "Used to Change Message to send When Ticket is Closed.",usage="   :")
async def close_msg(ctx):
	def author_check(msg):
		return msg.author == ctx.author and msg.channel == ctx.channel
	with open("configuration.json", "r") as config: 
		server_json = json.load(config)
	try:
		await ctx.send(embed = discord.Embed(title = 'Message' , description = 'What Message You would Like to Post When a You Close A Query ? ' , color=0xff5733 ) )
		server_json['DM By Message'] = (await bot.wait_for( "message" , check = author_check )).content
		await ctx.send(embed= discord.Embed(title="Sucessfully Changed!"))
	except:
		await ctx.send(embed = discord.Embed( title = ":x: Error" , description = "You Entered Some Thing Wrong. Please Try Again!" , color = 0xFF0000 ) )
	with open('configuration.json','w') as json_file_open:
		json.dump(server_json,json_file_open,indent=4)
		json_file_open.close()


@tasks.loop(seconds=100)
async def send_json_backup():
	with open("configuration.json", "r") as config: 
		server_json = json.load(config)
	if server_json.get('Backup JSON',None):
		with open('configuration.json','rb') as json_file_open:
			send_file_chann=get(get(bot.guilds,id=server_json["client_server"]).channels,id=server_json['Backup JSON'])
			await send_file_chann.purge(limit=100000)
			await send_file_chann.send(file=discord.File(json_file_open,'server_data.json'))
			json_file_open.close()


@bot.event
async def on_message(message):
	with open("configuration.json", "r") as config: 
		server_json = json.load(config)
	if message.author.id != bot.user.id:
		if message.guild is None :
			if data.get("host_server",None) or data.get("client_server",None):
				if message.content in server_json["Welcome Words"]:
					await message.channel.send(embed=discord.Embed(title = "Greetings" ,description=f"{message.content[0].upper()}{message.content[1:]}! Please Tell Your Query So that Your Ticket Can be Opened!"))
				else:
					recieve_guild=get(bot.guilds,id=server_json["client_server"])
					check_if_query_exists=None
					for i in recieve_guild.channels:
						try:
							if i.topic==str(message.author.id):
								check_if_query_exists=i
						except:
							continue
					if check_if_query_exists:
						if check_if_query_exists.category_id != server_json["Open DM"]:
							await check_if_query_exists.edit(category = get(recieve_guild.channels , id =  server_json["Open DM"]))
							await message.channel.send(embed = discord.Embed(title="Query Opened" ,  description = server_json["DM Welcome Message"] ,color= 0x1900FF))
						if message.content:
							await check_if_query_exists.send(embed = discord.Embed(title = f"From - `{message.author}`"  , description = f"{message.content}" , color=0xff5733))
						else:
							await check_if_query_exists.send(f"From - `{message.author}`")
						for i in message.attachments:
							await check_if_query_exists.send(file=(await i.to_file()))
					else:
						check_if_query_exists=await recieve_guild.create_text_channel(f'{str(message.author)}',category=get(recieve_guild.channels , id = server_json["Open DM"]), position=0 , topic=message.author.id)
						if message.content:
							await check_if_query_exists.send(embed = discord.Embed(title = f"From - `{message.author}`"  , description = f"{message.content}",color=0xff5733))
						else:
							await check_if_query_exists.send(f"From - `{message.author}`")
						for i in message.attachments:
							await check_if_query_exists.send(file=(await i.to_file()))
						await message.channel.send(embed = discord.Embed(title="Query Opened" ,  description = server_json["DM Welcome Message"] ,color= 0x1900FF))
					await message.add_reaction("✅")
			else:
				embed=discord.Embed(title="Setup Incomplete", description="ModMail setup is Incomplete ask Server Admin To complete Setup in Order To Use ModMail! \n To Start Setus Type `&setup`", color=0xff0000)
				await message.channel.send(embed=embed)
			with open('configuration.json','w') as json_file_open:
				json.dump(server_json,json_file_open,indent=4)
				json_file_open.close()
		elif message.channel.topic:
			try:
				i_d=int(message.channel.topic)
				if not message.content.startswith(prefix):
					if message.content:
						await (get(get(bot.guilds,id=server_json["host_server"]).members,id=i_d)).send(embed = discord.Embed(title = f"From - `{message.author}`" , description = f"{message.content}" ,color= 0x1900FF))
					else:
						await (get(get(bot.guilds,id=server_json["host_server"]).members,id=i_d)).send(f"From - `{message.author}`")
					for i in message.attachments:
						await (get(get(bot.guilds,id=server_json["host_server"]).members,id=i_d)).send(file=(await i.to_file()))
					if message.content:
						await message.channel.send(embed = discord.Embed(title = f"From - `{message.author}`" , description = f"{message.content}" ,color= 0x1900FF))
					else:
						await message.channel.send(f"From - `{message.author}`")
					for i in message.attachments:
						await message.channel.send(file=(await i.to_file()))
					await message.delete()
				else:
					await bot.process_commands(message)
			except:
				await bot.process_commands(message)
		else:
			await bot.process_commands(message)


@bot.command(description ="Used to close Ticket of The user.",usage="   :")
async def close(ctx):
	with open("configuration.json", "r") as config: 
		server_json = json.load(config)
	await ctx.message.channel.purge(limit=1)
	await ctx.channel.send(embed = discord.Embed(title="Query Closed" ,  description = server_json["DM By Message"] ,color= 0x1900FF))
	await (get(get(bot.guilds,id=server_json["host_server"]).members,id=int(ctx.channel.topic))).send(embed = discord.Embed(title="Query Closed" ,  description = server_json["DM By Message"]   ,color= 0x1900FF))
	recieve_guild=get(bot.guilds,id=server_json["client_server"])
	await ctx.channel.edit(category = get(recieve_guild.channels , id = int(server_json["Closed DM"])))
	with open('configuration.json','w') as json_file_open:
		json.dump(server_json,json_file_open,indent=4)
		json_file_open.close()


@bot.command(usage="<member_id>   :",description="Used To open Ticket of a user using Member ID.")
async def open_dm(ctx , memberid):
	with open("configuration.json", "r") as config: 
		server_json = json.load(config)
	recieve_guild=get(bot.guilds,id=server_json["client_server"])
	member=(get(get(bot.guilds,id=server_json["host_server"]).members,id=int(memberid)))
	check_if_query_exists=None
	for i in recieve_guild.channels:
		try:
			if i.topic==str(memberid):
				check_if_query_exists=i
		except:
			continue
	if check_if_query_exists:
		await check_if_query_exists.edit(category = get(recieve_guild.channels , id =  server_json["Open DM"]))
	else:
		check_if_query_exists=await recieve_guild.create_text_channel(f'{str(member)}',category=get(recieve_guild.channels , id = server_json["Open DM"]),topic=memberid)
	await ctx.message.add_reaction("✅")
	with open('configuration.json','w') as json_file_open:
		json.dump(server_json,json_file_open,indent=4)
		json_file_open.close()
bot.run(token)