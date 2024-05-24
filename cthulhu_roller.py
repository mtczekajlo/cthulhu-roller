#!/usr/bin/env python3
import discord
import re
import logging
from os import environ
from random import randint

logging.basicConfig(level=logging.INFO)

bot = discord.Bot()

COL_CRIT_FAILURE = 0xBE29EC
COL_NORM_FAILURE = 0x800080
COL_NORM_SUCCESS = 0x415D43
COL_HARD_SUCCESS = 0x709775
COL_EXTR_SUCCESS = 0x8FB996
COL_CRIT_SUCCESS = 0xB3CBB9


class RollResult:
    def __init__(self):
        self.title = ""
        self.desc = ""
        self.foot = ""
        self.colour = 0x000000


def RollDie(min=0, max=9):
    result = randint(min, max)
    return result


def tens_as_str(i: int) -> str:
    if i == 0:
        return "00"
    return str(i * 10)


def ResolveDice(BonusDie, PenaltyDie, Threshold):
    TenResultPool = []
    TenResultPool.append(RollDie())

    TenResult = min(TenResultPool)
    OneResult = RollDie()

    if BonusDie and PenaltyDie:
        return "Can't chain bonus and penalty dice."

    for i in range(BonusDie):
        TenResultPool.append(RollDie())
        TenResult = min(TenResultPool)

    for i in range(PenaltyDie):
        TenResultPool.append(RollDie())
        TenResult = max(TenResultPool)

    TenResultPool.sort(reverse=True)

    if TenResult == 0 and OneResult == 0:
        CombinedResult = 100
    else:
        CombinedResult = TenResult * 10 + OneResult

    ret = RollResult()

    ret.desc = f"Result: **{str(CombinedResult)}**"

    if Threshold:
        HardThreshold = Threshold // 2
        ExtremeThreshold = Threshold // 5
        ret.foot = f"""{ret.foot}
Threshold: {Threshold}/{HardThreshold}/{ExtremeThreshold}"""
        if CombinedResult > Threshold:
            ret.foot = f"""{ret.foot}
{CombinedResult-Threshold} points to Success"""
        elif CombinedResult > HardThreshold:
            ret.foot = f"""{ret.foot}
{CombinedResult-HardThreshold} points to Hard Success"""
        elif CombinedResult > ExtremeThreshold:
            ret.foot = f"""{ret.foot}
{CombinedResult-ExtremeThreshold} points to Extreme Success"""

    if BonusDie:
        ret.foot = f"""{ret.foot}
Bonus dice: {BonusDie}"""
    if PenaltyDie:
        ret.foot = f"""{ret.foot}
Penalty dice: {PenaltyDie}"""

    if CombinedResult == 1:
        ret.title = "CRITICAL SUCCESS!"
        ret.colour = COL_CRIT_SUCCESS
    elif CombinedResult == 100:
        ret.title = "CRITICAL FAILURE!"
        ret.colour = COL_CRIT_FAILURE
    elif Threshold:
        if CombinedResult >= 96 and Threshold < 50:
            ret.title = "CRITICAL FAILURE!"
            ret.colour = COL_CRIT_FAILURE
        elif CombinedResult <= ExtremeThreshold:
            ret.title = "Extreme Success! (1/5)"
            ret.colour = COL_EXTR_SUCCESS
        elif CombinedResult <= HardThreshold:
            ret.title = "Hard Success! (1/2)"
            ret.colour = COL_HARD_SUCCESS
        elif CombinedResult <= Threshold:
            ret.title = "Success"
            ret.colour = COL_NORM_SUCCESS
        else:
            ret.title = "Failure"
            ret.colour = COL_NORM_FAILURE

    ret.foot = f"""{ret.foot}
Rolls: {" ".join([f"[ {tens_as_str(r)} ]" for r in TenResultPool])} [ {OneResult} ]"""

    return ret


def parseRoll(diceString):
    help = """
```
/croll [[number=1][die type]]...[[score][threshold]]

Test roll:
    <number>t  Threshold to determine success or failure
    <number>b  Bonus dice
    <number>p  Penalty dice
Die roll:
    <number>d/k<number>+/-<number>  Custom dice with optional modifier

Examples:
    /croll
    Result: 36
    Rolls: [ 30 ] [ 6 ]

    /croll 60t
    Hard Success! (1/2)
    Result: 24
    Threshold: 60/30/12
    Rolls: [ 20 ] [ 4 ]

    /croll b
    Result: 35
    Bonus dice: 1
    Rolls: [ 70 ] [ 30 ] [ 5 ]

    /croll 2p70t
    Failure
    Result: 74
    Threshold: 70/35/14
    Penalty dice: 2
    Rolls: [ 70 ] [ 50 ] [ 00 ] [ 4 ]

    /croll d10
    Result: 8
    Rolling 1d10
    Rolls: [ 8 ]

    /croll 2k6+2
    Result: 9
    Rolling 2d6+2
    Rolls: [ 5 ] [ 2 ]
```
"""
    fail = (
        """
Unable to parse dice command. Usage:
"""
        + help
    )

    if diceString == "help":
        return help

    diceString = diceString.replace(" ", "")

    pattern = r"((\d+)?[dk]\d+)?([+-]\d+)?|(\d+?t)?|(\d+?[bp])?"
    matches = re.split(pattern, diceString)
    matches = [m for m in matches if m]

    dice = None
    sides = None
    threshold = None
    modifier = 0
    bonus = 0
    penalty = 0

    try:
        for match in matches:
            if any(c in match for c in ["d", "k"]):
                if "d" in match:
                    delimiter = "d"
                else:
                    delimiter = "k"
                dice, sides = list(map(lambda x: int(x or 1), match.split(delimiter)))
            elif any(c in match for c in ["+", "-"]):
                modifier = int(match)
            elif "t" in match:
                threshold = int(match.replace("t", ""))
            elif "b" in match:
                bonus, _ = list(map(lambda x: int(x or bonus + 1), match.split("b")))
            elif "p" in match:
                penalty, _ = list(
                    map(lambda x: int(x or penalty + 1), match.split("p"))
                )
    except Exception as e:
        print(e)
        return fail

    if dice and (threshold or penalty or bonus):
        return fail

    ret = RollResult()

    if dice:
        ret.foot = f"Rolling {dice}d{sides}"
        if modifier:
            ret.foot = f"{ret.foot}{modifier:+}"
        rolls = [RollDie(1, int(sides)) for _ in range(int(dice))]
        ret.foot = f"""{ret.foot}
Rolls: {" ".join([f"[ {r} ]" for r in rolls])}"""
        total = sum(rolls) + modifier
        ret.desc = f"Result: **{str(total)}**"
    else:
        if bonus > penalty:
            bonus -= penalty
            penalty = 0
        elif penalty > bonus:
            penalty -= bonus
            bonus = 0
        else:
            bonus = 0
            penalty = 0
        ret = ResolveDice(bonus, penalty, threshold)

    return ret


@bot.slash_command(name="croll")
async def cthulhu_roll(
    ctx: discord.ApplicationContext,
    dice: discord.Option(
        str, "Dice string. Enter 'help' for more details.", default=""
    ),
):
    """
    Call of Cthulhu dice roll.
    """
    result = parseRoll(dice)
    if isinstance(result, str):
        await ctx.respond(result)
    else:
        em = discord.Embed(
            title=result.title, description=result.desc, colour=result.colour
        )
        em.set_footer(text=result.foot)
        await ctx.respond(embed=em)


def main():
    token = environ["DISCORD_TOKEN"]
    bot.run(token)


if __name__ == "__main__":
    main()
