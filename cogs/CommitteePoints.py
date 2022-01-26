import requests
from discord.ext import commands
import tools



class CommitteePoints(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def points(self, ctx, arg1):
        results = await tools.querySelect(f"""SELECT * FROM CommitteePoints WHERE id = "{arg1}";""")
        await ctx.channel.send(f"{results[0][0]} has {results[0][1]} points")
        
    @commands.command()
    async def addPoints(self, ctx, arg1, arg2):
        points = await tools.querySelect(f"""SELECT * FROM CommitteePoints WHERE id = "{arg1}";""")
        points2 = points[0][1] + int(arg2)
        await tools.queryInsert(f"""UPDATE CommitteePoints SET points = {points2} WHERE id = "{arg1}";""")



def setup(client):
    client.add_cog(CommitteePoints(client))
