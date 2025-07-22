import discord
import asyncio
import logging
import random


from discord.ext import commands
from discord import User
from dataclasses import dataclass, field

bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())


@dataclass
class BotConfig:
    Token: str = ""
    status_text: str = "Online"
    activity_type: str = "Playing with mikeys smelly balls"

logging.basicConfig(level=logging.INFO)

@bot.event
async def on_command_error(ctx, error):
    print(f"⚠️ Command error: {error}")
    await ctx.send(f"⚠️ Error: {error}")



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    await bot.change_presence(activity=discord.Game(name="big smelly "))

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason="no reason"):

    if not ctx.author.guild_permissions.administrator:
        return await ctx.reply("❌ You need to be an Admin to use this command.")
    
    if ctx.author.top_role <= member.top_role:
        return await ctx.reply("❌ You can't ban someone with an equal or higher role.")

    if member == None:
        await ctx.reply('you didnt specify the person to kick retard')
    if member == ctx.guild.me:
        await ctx.reply("you cant ban your self")

    try:
        await member.kick(reason=reason)
        await ctx.reply(f"member {member} has been kicked")

        log_channel = ctx.guild.get_channel(1283871861754560563)

        if log_channel:
            await log_channel.send(
                f"{ctx.author} kicked {member} for {reason}"
                )
    except Exception as e:
        await ctx.reply(f"error: {e}")

@bot.command()
async def ban(ctx, user: User = None, *, reason="no reason"):
    if user is None:
        await ctx.reply('you didnts specify the member to ban')


    if user.id == ctx.guild.me.id:
        await ctx.reply('cant ban your self ')


    bans = []
    async for ban_entry in ctx.guild.bans():
        bans.append(ban_entry)

    if any(ban_entry.user.id == user.id for ban_entry in bans):
        return await ctx.reply("⚠️ That user is already banned.")


    try:
        await ctx.guild.ban(user, reason=reason)
        await ctx.reply(f"{user} has been banned \n reason: {reason}")

       

        log_channel = ctx.guild.get_channel(1283871861754560563)

        if log_channel:
                await log_channel.send(f"{ctx.author} banned {user} \n for {reason}")
    except Exception as e:
            await ctx.reply(f"error {e}")

@bot.command()
async def rpc(ctx):
    await ctx.reply("Rock, Paper, or Scissors? Type your choice below:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['rock', 'paper', 'scissors']

    try:
        msg = await bot.wait_for('message', check=check, timeout=15.0)
    except asyncio.TimeoutError:
        return await ctx.reply("⏰ You took too long to respond!")

    user_choice = msg.content.lower()
    bot_choice = random.choice(['rock', 'paper', 'scissors'])

    result = None
    if user_choice == bot_choice:
        result = "It's a tie!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'scissors' and bot_choice == 'paper') or \
         (user_choice == 'paper' and bot_choice == 'rock'):
        result = "You win! 🎉"
    else:
        result = "I win! 😈"

    await ctx.send(f"You chose **{user_choice}**.\nI chose **{bot_choice}**.\n**{result}**")
 
@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send(f'{slapped} just got slapped for: \n {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    if amount <= 0:
        await ctx.reply("must be a number bigger than 0")
    try:
        await ctx.channel.purge(limit=amount +1)
        await ctx.reply("deleted" + len(amount) + "of messages" )
    except Exception as e:
        await ctx.reply(e)

@bot.command()
async def bj(ctx):
    import random
    import asyncio

    cards: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    player_cards = [random.choice(cards), random.choice(cards)]
    dealer_cards = [random.choice(cards), random.choice(cards)]

    def hand_total(hand):
        return sum(hand)

    await ctx.reply(f"dealer has {dealer_cards[0]}\nyou have {player_cards[0]} and {player_cards[1]}\nhit or stay?")


    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['hit', 'stay']

    while True:
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply("you ran out of time")
            return

        if msg.content.lower() == "hit":
            new_card = random.choice(cards)
            player_cards.append(new_card)
            total = hand_total(player_cards)
            await ctx.reply(f"You drew a {new_card}. (total: {total})")
            if total == 21:
                await ctx.reply("you hit 21!!")
                break
            elif total > 21:
                await ctx.reply(f"you busted your card total is {total}")
                return

        elif msg.content.lower() == "stay":
            break

    while hand_total(dealer_cards) < 17:
        dealer_cards.append(random.choice(cards))

    player_total = hand_total(player_cards)
    dealer_total = hand_total(dealer_cards)

    await ctx.reply(f"dealer's total(total: {dealer_total})")

    if dealer_total > 21 or player_total > dealer_total:
        await ctx.reply("you win")
    elif dealer_total == player_total:
        await ctx.reply("issa tie folk")
    else:
        await ctx.reply("dealer winds")

bot.run(BotConfig().Token)