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


import linecache

token = os.environ['token']
client = commands.Bot(command_prefix="&", intents=discord.Intents.all())



@client.command()
@commands.has_role("Moderator [MR]")
async def status(self, ctx:commands.Context):
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



@client.event
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
				channel = await guild.create_text_channel(msg.author.name, category=category, soverwrites=overwrites, reason=f"Create a ticket for {msg.author}")
				channel_id = channel.id
				print(channel_id)
				with open(f"Tickets/{msg.author.id}.txt", "w") as file:
					file.write(f"{channel_id}\n{msg.author.id}")
				em = discord.Embed(title="New Ticket", description="Thanks for creating a ticket. Support staff will get intouch shortly", colour=discord.Colour.green())
				await msg.reply(embed=em, mention_author=False)
				em = discord.Embed(title=f"New Ticket for {msg.author}", description=f"To reply to this message, type `&reply {msg.author.id} <message>`. To get a list of commands, type `&help`. To chat with staff, just type below. Any problems, contact one of the Developers", colour=discord.Colour.blue())
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
				
			
				
@client.command()
@
			


keep_alive()

client.run(token)

