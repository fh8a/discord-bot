import discord
import asyncio
import logging
import random
import json
import os

from discord.ext import commands
from discord import User
from dataclasses import dataclass, field

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

"""
only thing i really used chat gpt for was the currency part (.json) so prolly 10-15 is inspired from chat gpt code

"""

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
    await bot.change_presence(activity=discord.Game(name=BotConfig().activity_type))

    try:
        await bot.user.edit(username="Kawaii cute Cat Girl")
        print("Username changed.")
    except Exception as e:
        print(f"Failed to change username: {e}")
    # Change avatar by loading a file

    try:
        with open("/home/teeski/Downloads/kawaii.jpeg", "rb") as f:
            avatar_bytes = f.read()
        await bot.user.edit(avatar=avatar_bytes)
        print("Avatar changed.")
    except Exception as e:
        print(f"Failed to change avatar: {e}")


@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="📖 Bot Help",
        description="Here are my available commands:",
        color=discord.Color.gold()
    )

    embed.add_field(name="🧪 `!eightball [question]`", value="Ask the magic 8-ball a question.", inline=False)
    embed.add_field(name="💖 `!ship @user1 @user2`", value="See how much two users are meant to be.", inline=False)
    embed.add_field(name="🔒 `!rpc`", value="play rock papa scissa.", inline=False)
    embed.add_field(name="🤣 `!blackjack`", value="gamble sum g.", inline=False)
    embed.add_field(name="👋😵 `!slap`", value="slap a nigga silly.", inline=False)
    embed.add_field(name="🏳️‍🌈 `!gayscale`", value="test how gay you are g", inline=False)
    embed.add_field(name="🪙 `!coinflip`", value="coinflip! 50/50 chance", inline=False)
    embed.add_field(name="💸 `!checkbalance`", value="check the amount of money u have", inline=False)
    embed.add_field(name="❓ `!help`", value="Shows this help message.", inline=False)


    embed.set_footer(text="Use !help [command] for more info on a specific command.")

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason="no reason"):

    if not ctx.author.guild_permissions.administrator:
        return await ctx.reply("❌ You need to be an Admin to use this command.")
    
    if ctx.author.top_role <= member.top_role:
        return await ctx.reply("❌ You can't ban someone with an equal or higher role.")

    if member == None:
        await ctx.reply('>.< you didnt sp')
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
    await ctx.reply("Hehe~ Daddy~ wanna play Rock, Paper, or Scissors? Tell me your choice and make me purr~ 😘💦")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['rock', 'paper', 'scissors']

    try:
        msg = await bot.wait_for('message', check=check, timeout=15.0)
    except asyncio.TimeoutError:
        return await ctx.reply("⏰ Senpai~ you took too long... Now I'm all wet and lonely waiting for you~ 💦💔")

    user_choice = msg.content.lower()
    bot_choice = random.choice(['rock', 'paper', 'scissors'])

    if user_choice == bot_choice:
        result = "Aww~ a tie! Means we’re evenly matched... or maybe I’m just teasing you~ 💞😳"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'scissors' and bot_choice == 'paper') or \
         (user_choice == 'paper' and bot_choice == 'rock'):
        result = "Yattaaa~ you win, senpai! Come reward me with some kisses~ 💖💋"
    else:
        result = "Ehehe~ I win! Better luck next time, or maybe I’ll just have to punish you myself~ 😈💦"

    await ctx.send(f"💋 You chose **{user_choice}**~\nI chose **{bot_choice}**~\n**{result}** 💕")

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='being a naughty little cutie~ 😘'):
    if not members:
        await ctx.reply("Slap who, huh? Maybe I should slap *you* instead~ 😏💥")
        return
    slapped = ", ".join(x.mention for x in members)
    await ctx.send(f"💢 *SLAP!!* {slapped} got a spicy spanking! Hope they liked it as much as I did~ 😳💥💦\nBecause: *{reason}*")

@bot.command()
async def mock(ctx, *, text):
    mocked = ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
    await ctx.send(mocked)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    if amount <= 0:
        await ctx.reply("That’s too small, cutie~ Gotta be bigger to clean up all those dirty messages~ >///<")
        return
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.reply(f"✨ Cleared {amount} naughty messages~ All fresh and ready for more fun~ 💖💦")
    except Exception as e:
        await ctx.reply(f"Oopsie~ something naughty happened: {e}")

class currency:
    def __init__(self, currency_file: str = "/home/teeski/Downloads/bot/currency.json"):
        self.balance_file = currency_file
        if os.path.exists(self.balance_file):
            try:
                with open(self.balance_file, 'r') as f:
                    self.user_balances = json.load(f)
                    self.user_balances = {int(k): v for k, v in self.user_balances.items()}
            except json.JSONDecodeError:
                self.user_balances = {}
        else:
            self.user_balances = {}

    def save_balances(self):
        with open(self.balance_file, "w") as f:
            json.dump(self.user_balances, f)

my_currency = currency()

@bot.command()
async def checkbalance(ctx):
    user_id = ctx.author.id
    balance = my_currency.user_balances.get(user_id, 0)
    await ctx.reply(f"✨ UwU~ You have **{balance}** shiny coins, senpai~ Spend 'em on me and make me happy~ 💸💖")

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    try:
        user_id = ctx.author.id
        receiver_id = member.id
        if my_currency.user_balances.get(user_id, 0) < amount:
            await ctx.reply("⛔ Teehee~ you don’t have enough coins, silly~ Maybe try begging? 💸😳")
            return

        my_currency.user_balances[user_id] -= amount
        my_currency.user_balances[receiver_id] = my_currency.user_balances.get(receiver_id, 0) + amount
        my_currency.save_balances()
        await ctx.reply(f"✨ Sent **{amount}** sparkly coins to {member.mention}~ Hope they make you both blush~ 💞😳")
    except Exception as e:
        await ctx.reply(f"Oopsie~ {e}")

@bot.command()
async def bj(ctx):
    user_id = ctx.author.id
    if user_id not in my_currency.user_balances:
        my_currency.user_balances[user_id] = 1000

    balance = my_currency.user_balances[user_id]
    await ctx.reply(f"💰 You have **${balance}** coins, senpai~ How much do you wanna bet? Don’t keep me waiting, I’m getting wet~ 💦")

    def bet_check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        bet_msg = await bot.wait_for("message", timeout=30.0, check=bet_check)
        bet = int(bet_msg.content)
    except asyncio.TimeoutError:
        await ctx.reply("⏰ Oopsie~ you took too long! I was already getting all hot and bothered~ 😳💦")
        return

    if bet > balance:
        await ctx.reply(f"😖 You can’t bet more than what you have, silly~ (${balance}) Try again, baka~")
        return
    if bet <= 0:
        await ctx.reply("Uhm... bet a positive amount, cutie~ >///<")
        return

    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    player_cards = [random.choice(cards), random.choice(cards)]
    dealer_cards = [random.choice(cards), random.choice(cards)]

    def hand_total(hand):
        return sum(hand)

    await ctx.reply(f"🎴 Dealer shows **{dealer_cards[0]}**, you have **{player_cards[0]}** & **{player_cards[1]}**~ Hit or stay, daddy? I’m yours to command~ 😈💖")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['hit', 'stay']

    while True:
        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply("⏰ So slow~ I was getting impatient... Come on, daddy~ 🥺💦")
            return

        if msg.content.lower() == "hit":
            new_card = random.choice(cards)
            player_cards.append(new_card)
            total = hand_total(player_cards)
            await ctx.reply(f"✨ You drew a **{new_card}**! Total is **{total}**~ Oooh, this is getting exciting~ 😳💦")
            if total == 21:
                await ctx.reply("🎉 21!!! You're so good at this, senpai~ You make me melt~ 💕🔥")
                break
            elif total > 21:
                await ctx.reply(f"💔 Busted at **{total}**... You lost **${bet}**~ Don’t cry, daddy~ I’ll make it up to you~ 🥺💦")
                my_currency.user_balances[user_id] -= bet
                my_currency.save_balances()
                await ctx.reply(f"💸 Your new balance is **${my_currency.user_balances[user_id]}**~ Stay strong and come back for more~ 💪💖")
                return
        elif msg.content.lower() == "stay":
            await ctx.reply("Ooh~ You stay? Good boy~ Let’s see how I do~ 😈")
            break

    while hand_total(dealer_cards) < 17:
        dealer_cards.append(random.choice(cards))

    player_total = hand_total(player_cards)
    dealer_total = hand_total(dealer_cards)

    await ctx.reply(f"🃏 Dealer’s total is **{dealer_total}**~!")

    if dealer_total > 21 or player_total > dealer_total:
        await ctx.reply(f"🌟 You win~! You earned **${bet}**~ Mommy's so proud of you~ 💖💦")
        my_currency.user_balances[user_id] += bet
    elif dealer_total == player_total:
        await ctx.reply("😗 It’s a tie~ No coins lost! Lucky you~ Let’s play again, cutie~ 💕")
    else:
        await ctx.reply(f"😭 Dealer wins... You lost **${bet}**... Don’t be sad, daddy~ I’m here to cheer you up~ 💔💦")
        my_currency.user_balances[user_id] -= bet

    my_currency.save_balances()
    await ctx.reply(f"💰 Your new balance is **${my_currency.user_balances[user_id]}**~ Can’t wait for our next game~ 😘")

@bot.command()
async def coinflip(ctx):
    coins = random.choice(['✨ Heads~ UwU 💦', '💫 Tails~ Nyaa 💦'])
    await ctx.reply(f"Flip~! You got **{coins}**! Lucky you, senpai~ Wanna flip again for a prize? 😘")

@bot.command()
async def eightball(ctx):
    eight_ball_responses = [
        "💖 It is certain, senpai~ I’m sure of it~ 😘",
        "💫 Without a doubt, daddy~ I know you want it~ 💦",
        "✨ Yes definitely, and I wanna help you with that~ 💕",
        "🩷 You can rely on it, baby~ I’m all yours~ 😈",
        "🔮 Most likely, and you’ll get your reward~ 💦",
        "🌸 Outlook good, daddy~ Keep dreaming about me~ 😘",
        "Yesh~ Can’t wait to see you~ 💕",
        "Signs point to yes, baby~ You’re making me blush~",
        "🤔 Hmm... try again~ I wanna hear you say it~ 💖",
        "Ask again later, pwease~ I’m teasing you~ 😜",
        "Better not say~ I wanna keep you waiting, nya~ >///<",
        "Can’t predict now, srry~ But I’m thinking naughty thoughts~ 💦",
        "Concentrate and try again, daddy~ I’m feeling frisky~",
        "Nooope~ Not yet~ But soon~ 😈",
        "My reply is nooo~ But only ‘cause I want more teasing~ 🥺",
        "Source says no~ But you can change my mind, cutie~",
        "Not so good~ Maybe later when you behave better~ 💕",
        "Very doubtful~ But I’m always open to bribery~ 💦",
        "I’m just a kawaii bot~ But I want you so bad~ >w<",
        "Ask your mama~ She knows what you want~ 💅",
        "Lol nu uh~ But I’m still here for you~ 😘",
        "Maybe if you believe hard enough~ And beg me~ ✨",
        "In another timeline~ We’d be together all night~ 💖",
    ]
    rando = random.choice(eight_ball_responses)
    await ctx.reply(f"{rando}~ 💕")

@bot.command()
async def gayscale(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    try:
        scale = random.randint(1, 100)
        if scale > 75:
             await ctx.reply(f"🏳️‍🌈 Omg~ {member.mention} is **{scale}%** gay!! So sparkly and juicy~ Wanna show me? 🌈💦✨")
        else:
            await ctx.reply(f"🏳️‍🌈 {member.mention} is only **{scale}%** gay uwu~ Be Mommy's Good Boy >.< :p~ 💕😳💦")
    except Exception as e:
        await ctx.reply(f"Oopsie~ error nya~ 😿\n{e}")

@bot.command()
async def ship(ctx, user1: discord.Member, user2: discord.Member):
    luv_percent = random.randint(1, 100)
    if luv_percent >= 90:
        description = "💘 Made for each other~ So doki doki, let me ship you hard~ 💞💦"
    elif luv_percent >= 70:
        description = "💕 They def have a spark~ Owo, so spicy! 😳"
    elif luv_percent >= 50:
        description = "🤭 Could be a cute couple... maybe we’ll see some steamy moments~"
    elif luv_percent >= 25:
        description = "😬 Might not last long, but I’ll enjoy watching~ Cry me a river~"
    else:
        description = "💔 Run away before it’s too late, but I’m kinda turned on by this drama~"

    embed = discord.Embed(
        title="💞 Love Compatibility 💞",
        description=f"{user1.display_name} 💖 {user2.display_name} = **{luv_percent}%**\n{description}",
        color=discord.Color.pink()
    )

    embed.set_footer(text="Kyaaa~ Use responsibly, or I might get jealous~ 💘😈")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(BotConfig().Token)
