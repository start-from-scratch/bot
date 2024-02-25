import discord
from discord import application_command, Option, Embed, Color
from discord.ext import commands
from logs import logger
from time import time

with open("token.txt", "r") as f:
  token = f.read()
  f.close()

with open("id.txt", "r") as f:
  id = int(f.read())
  f.close()
  
start = int(time())          #voir uptime 
bot = commands.Bot()


def create_embed(titre, description, auteur,couleur ):
    embed = discord.Embed(title=titre, description=description, color=couleur)
    #embed.add_field(name="Champ 1", value="Valeur 1")
    #embed.set_author(name= auteur)
    #embed.set_thumbnail(url=auteur_url)
    embed.set_footer(text=f"Information requested by: {auteur}")
    return embed

@bot.event
async def on_ready() -> None:
    await bot.get_channel(id).send(f"Bot {bot.user.mention} demarré :green_circle: (Version Beta)") #envoie un msg dans le salon id au demarrage du bot

@bot.event
async def on_message_delete(message):
    if message.mentions and not message.author.bot:
        for user in message.mentions:
            channel = bot.get_channel(message.channel.id)
            await user.send(f"Vous avez été ghost ping par {message.author.name} dans le salon {channel.name} du serveur {message.guild.name}", )
            embed = create_embed("Ghost Ping","Un Ghost ping viens d'etre detecte", bot.user.name, discord.Color.random())
            embed.add_field(name="Author:", value= message.author.mention, inline = True)
            embed.add_field(name="Mention:", value=user.mention, inline = True)
            embed.add_field(name="Channel:", value=f"ID: {message.channel.id} \n Name: {message.channel.name}", inline = False)
            await channel.send(embed=embed)

                           
@bot.slash_command(
  name = "say",
  description = "Fais dire quelque chose au bot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx: application_command(), 
  message: Option(str)
) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

@bot.slash_command(
    name = "infos",
    description = "Avoir des Informations sur le bot" 
)
async def infos(ctx):
    embed = create_embed("Infos", f"{bot.user.mention} ping is {int(bot.latency * 1000)} ms \n A été lancé <t:{start}:R> \n Actuellement dans {len(bot.guilds)} serveurs", ctx.author.name, "#008FFF")
    await ctx.respond(embed=embed)


@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
async def ping(ctx):
    embed = create_embed("Ping", f"{bot.user.mention} ping is {int(bot.latency * 1000)} ms", ctx.author.name,"#FFA900")
    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "help",
    description = "Liste des commandes disponibles" 
)
async def help(ctx):
    embed = create_embed("Help", f"Commandes Disponible : \n `/ping` - Avoir le ping du bot \n `/infos` - Avoir des Informations sur le bot \n `/help` - Liste des commandes disponibles \n `/say` - Fais dire quelque chose au bot (admin only)", ctx.author.name, "#200B9C")
    await ctx.respond(embed=embed)

@bot.slash_command(
    name= "embed",
    description="Crée un embed" 
)
async def embed(ctx, 
  titre: Option(str), 
  description: Option(str),
  couleur: Option(str)
):
  embed = create_embed(titre, description, ctx.author.name,couleur)
  await ctx.respond(embed=embed)




bot.run(token)
