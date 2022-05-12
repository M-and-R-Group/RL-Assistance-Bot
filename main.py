import os
import discord
from discord import Member
from discord.utils import get
import random
import asyncio
import time
from discord.ext import commands, tasks
from random import choice
from webserver import keep_alive
import random
from random import randint
import sys
import datetime
from discord_slash import SlashCommand
import linecache

token = os.environ['token']
client = commands.Bot(command_prefix="rl!", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)




@slash.slash(name="Status", description="Get the status of the bot")
async def status(ctx):
    curr_time = time.localtime()
    curr_clock = time.strftime("%H:%M", curr_time)
    em = discord.Embed(title="RL Assistance is online! 😃", colour=discord.Colour.green())
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.send(embed=em)

@client.event
async def on_ready():
	print("Bot is online and ready to check tickets!")
	await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening,
                                  name=f" tickets"))



@client.listen("on_message")
async def on_message(msg):
	if isinstance(msg.channel, discord.channel.DMChannel):
		
		if msg.author.id == 927534336692064337:
			pass
		else:
			print('1')
			guild =  client.get_guild(916352060520267847)
			path = f"Tickets/{msg.author.id}.txt"

			if os.path.exists(path)==True:

				ticket_data = open(f"Tickets/{msg.author.id}.txt","r")
				channel_id = linecache.getline(f"Tickets/{msg.author.id}.txt", 1)
				print(channel_id)
				channel_id = int(channel_id)
				channel = client.get_guild(916352060520267847).get_channel(channel_id)
				print(channel)
				em = discord.Embed(title="New Message", description=f"{msg.content}", colour=discord.Colour.green())
				em.set_footer(text=f"{msg.author} | {msg.author.id}")
				em.timestamp = datetime.datetime.utcnow()
				await channel.send(embed=em)
				await msg.add_reaction('✅')
				confirm = await msg.reply("Message sent, support will get back to you soon")
				await asyncio.sleep(2)
				await confirm.delete()
			else:

				print('2')
				modmailperms = 972831136705314816
				modmailperms = discord.utils.get(guild.roles, id=modmailperms)

				ticket_log = client.get_channel(972880414119186432)
				overwrites = {
    				guild.default_role: discord.PermissionOverwrite(view_channel=False),
    				modmailperms: discord.PermissionOverwrite(view_channel=True)
				}
				category = discord.utils.get(guild.categories, name = "Tickets")
				channel = await guild.create_text_channel(msg.author.name, category=category, overwrites=overwrites, reason=f"Create a ticket for {msg.author}")
				channel_id = channel.id
				print(channel_id)
				with open(f"Tickets/{msg.author.id}.txt", "w") as file:
					file.write(f"{channel_id}\n{msg.author.id}")
				em = discord.Embed(title="New Ticket", description="Thanks for creating a ticket. In the meantime, please describe the reason for this ticket in as much detail as possible. If you don't get a reply in 24 hours, please ping a staff member.\n\nMisuse of the ticketing system will result in action being taken. We reserve the right to refuse assistance to any user without explanation. Your data (User ID) is stored by the bot so it can DM you support staff responses. You reserve the right to have your data be removed upon request, however, your data will be deleted from this system when the ticket is closed.", colour=discord.Colour.green())
				await msg.reply(embed=em, mention_author=False)
				em = discord.Embed(title=f"New Ticket for {msg.author}", description=f"To reply to this message, type `/reply {msg.author.id} <message>`. To get a list of commands, type `/help`. To chat with staff, just type below. Any problems, contact one of the Developers", colour=discord.Colour.blue())
				em.add_field(name="\n\n**User**",value=f"{msg.author.mention}\n{msg.author.id}", inline=True)
				#user = msg.author
				#for role in user.roles:
					#if role.name != "@everyone":
						#mention.append(role.mention)
				#b = ", ".join(mention)
				#em.add_field(name="**Roles**", value=b, inline=True)
				await channel.send(embed=em)
				em = discord.Embed(title="New Message", description=f"{msg.content}", colour=discord.Colour.green())
				em.set_footer(text=f"{msg.author} | {msg.author.id}")
				em.timestamp = datetime.datetime.utcnow()
				await channel.send(embed=em)
				ticket_logs = client.get_channel(972880414119186432)
				em = discord.Embed(title="New Ticket", description=f"{msg.author.mention} opened a new ticket. Go to {channel.mention}")
				em.timestamp = datetime.datetime.utcnow()
				log = await ticket_logs.send(embed=em)
				with open(f"Tickets/{msg.author.id}.txt", "a") as file:
					file.write(f"\n{log.id}\n0")
				
			
				
@slash.slash(name = "Claim", description="Claim a ticket using the user's ID")
@commands.has_role(972831136705314816)
async def claim(ctx, member: discord.Member):
	print(member)
	path = f"Tickets/{member.id}.txt"
	if os.path.exists(path)==True:
		support_staff = ctx.author.id
		message_claimed = linecache.getline(f"Tickets/{member.id}.txt", 4)
		if message_claimed == "0":
			with open(f"Tickets/{msg.author.id}.txt", "a") as file:
						file.write(f"1\n{ctx.author.id}")
			em = discord.Embed(title="✅ | Ticket Claimed", description="You have successfully claimed the ticket. A message will be sent to the user.", colour=discord.Colour.green())
			em.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=em)
			em = discord.Embed(title="Ticket Claimed", description=f"You're ticket has been claimed by {ctx.author.mention}. You should recieve a message shortly.",colour=discord.Colour.green())
			em.timestamp = datetime.datetime.utcnow()
			member = linecache.getline(f"Tickets/{member.id}.txt", 2)
			member = int(member)
			member=client.get_member(member)
			await member.send(embed=em)
		elif message_claimed == "1":
			support_staff = linecache.getline(f"Tickets/{member.id}.txt", 5)
			support_staff = int(support_staff)
			support_staff = client.get_user(support_staff)
			em = discord.Embed(title="❌ | Claim Ticket", description=f"Ticket has already been claimed by {support_staff.mention}", colour=discord.Colour.red())
			em.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=em)
		
	else:
		em = discord.Embed(title="❌ | Ticket Error", description="This ticket cannot be found. This may be because the ticket file is corrpupted or the ticket has been resolved.", colour=discord.Colour.red())
		em.timestamp = datetime.datetime.utcnow()
		await ctx.reply(embed=em, hidden=True)

@slash.slash(name="Reply", description="Reply to the ticket")
@commands.has_role(972831136705314816)
async def reply(ctx, member: discord.Member, *, message):
	path = f"Tickets/{member.id}.txt"
	if os.path.exists(path)==True:
		try:
			em = discord.Embed(title="📨 | Message Recieved", description=f"You have recieved a message from {ctx.author.mention}:\n\n{message}",colour=discord.Colour.blue())
			em.timestamp = datetime.datetime.utcnow()
			await member.send(embed=em)
			em = discord.Embed(title="📨 | Message Sent", description=f"{message}",colour=discord.Colour.blue())
			em.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=em)
		except:
			em = discord.Embed(title="❌ | Message Error", description=f"There was an error, please try again",colour=discord.Colour.red())
			em.timestamp = datetime.datetime.utcnow()
			await ctx.reply(embed=em, hidden=True)
			
	else:
		em = discord.Embed(title="❌ | Message Error", description=f"There is no ticket for this user",colour=discord.Colour.red())
		em.timestamp = datetime.datetime.utcnow()
		await ctx.reply(embed=em, hidden=True)

@slash.slash(name="Close", description="Close the ticket")
@commands.has_role(972831136705314816)
async def close(ctx, member:discord.Member, message=None):
	path = f"Tickets/{member.id}.txt"
	if os.path.exists(path)==True:
		#try:
			if message == None:
				channel = linecache.getline(f"Tickets/{member.id}.txt", 1)
				channel = int(channel)
				channel = client.get_channel(channel)
				await channel.delete(reason=f"Ticket Closed by {ctx.author}")
				em = discord.Embed(title="📨 | Ticket Closed", description=f"Your ticket has been closed. If you did not want this, please open a new ticket",colour=discord.Colour.blue())
				em.timestamp = datetime.datetime.utcnow()
				await member.send(embed=em)
				message_claimed = linecache.getline(f"Tickets/{member.id}.txt", 3)
				message_claimed = int(message_claimed)
				em = discord.Embed(title="📨 | Ticket Closed", description=f"{member.mention}'s ticket was closed by {msg.author.mention}",colour=discord.Colour.blue())
				em.set_footer(text=f"{member.id} | Time Displayed is date ticket closed:")
				em.timestamp = datetime.datetime.utcnow()
				channel = bot.get_channel(972880414119186432)
				message_claimed_id = await channel.fetch_message(message_claimed)
				await channel.message_claimed_id.edit(embed=em)
				os.remove(f"Tickets/{member.id}")
			else:
				channel = linecache.getline(f"Tickets/{member.id}.txt", 1)
				channel = int(channel)
				channel = client.get_channel(channel)
				await channel.delete(reason=f"Ticket Closed by {ctx.author}")
				em = discord.Embed(title="📨 | Ticket Closed", description=f"Your ticket has been closed because:```{message}```\nf you did not want this, please open a new ticket",colour=discord.Colour.blue())
				em.timestamp = datetime.datetime.utcnow()
				await member.send(embed=em)
				message_claimed = linecache.getline(f"Tickets/{member.id}.txt", 3)
				message_claimed = int(message_claimed)
				em = discord.Embed(title="📨 | Ticket Closed", description=f"{member.mention}'s ticket was closed by {msg.author.mention}.\n\nReason:```{message}```",colour=discord.Colour.blue())
				em.set_footer(text=f"{member.id} | Time Displayed is date ticket closed:")
				em.timestamp = datetime.datetime.utcnow()
				channel = bot.get_channel(972880414119186432)
				message_claimed_id = await channel.fetch_message(message_claimed)
				await channel.message_claimed_id.edit(embed=em)
				os.remove(f"Tickets/{member.id}")
			
		#except:
			#em = discord.Embed(title="❌ | Close Error", description=f"I encountered a problem, please try again",colour=discord.Colour.red())
			#em.timestamp = datetime.datetime.utcnow()
			#await ctx.reply(embed=em, hidden=True)
	else:
		em = discord.Embed(title="❌ | Close Error", description=f"There is no ticket for this user",colour=discord.Colour.red())
		em.timestamp = datetime.datetime.utcnow()
		await ctx.reply(embed=em, hidden=True)
			
		
		
keep_alive()

client.run(token)

