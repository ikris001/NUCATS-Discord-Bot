import random
import requests
from discord.ext import commands
import tools



class CodeWars(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx, arg1):
        # checks if person exists
        await ctx.message.delete()
        response = requests.get("https://www.codewars.com/api/v1/users/" + arg1)
        if (response.status_code == 200):
            await tools.queryInsert(f"""INSERT INTO Codewars
                                VALUES ('{str(ctx.author)}', '{arg1}');""")
            # if exist add to array end and store in db
            await tools.log(self.client, "CODEWARS User {" + arg1 + "} added for " + str(ctx.author))
            await ctx.channel.send("CODEWARS User {" + arg1 + "} added for " + str(ctx.author), delete_after=30)
        else:
            # if don't exist error
            await tools.log(self.client, "api response error : " + str(response))
            await ctx.channel.send("api response error : " + str(response), delete_after=30)


    @commands.command()
    async def draw(self, ctx):
        response = await tools.querySelect(f"""SELECT * FROM Codewars;""")
        responseDict = {}
        for i in response:
            if(i[0] == "code"):
                id = i[1]
            else:
                responseDict[i[0]] = i[1]
        responseKeys = responseDict.keys()
        winner = random.sample(responseKeys, 1)[0]
        winnerUsername = responseDict[winner]
        await tools.log(self.client, f'Drawn is {winner}')
        response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername}/code-challenges/completed')
        resObject = response.json()
        for obj in resObject["data"]:
            if (obj["id"] == id):
                await tools.log(self.client, f'{winner} has  completed the challenge soo wins £5 pounds!!!')
                await ctx.channel.send(f'{winner} has  completed the challenge soo wins £5 pounds!!!')
                return 0
        await ctx.channel.send(f'{winner} has not completed the challenge soo we draw again')
        await tools.log(self.client, f'{winner} has not completed the challenge soo we draw again')
        return 0

    
    @commands.command()
    async def challenge(self, ctx, arg1):
        await tools.queryInsert(f"""DELETE FROM Codewars WHERE id = "code";""")
        await tools.queryInsert(f"""INSERT INTO Codewars
                                VALUES ('code', '{arg1}');""")

        
    @commands.command()
    async def listStat(self, ctx):
        response = await tools.querySelect(f"""SELECT * FROM Codewars;""")
        responseValues = [i[1] for i in response]
        challenge = await tools.querySelect(f"""SELECT * FROM Codewars WHERE id = "code";""")
        complete = 0;
        total = 0;
        for k in responseValues:
            total = total + 1
            out = False
            winner = str(k)
            response = requests.get(f'https://www.codewars.com/api/v1/users/{winner}/code-challenges/completed')
            resObject = response.json()
            try:
                for obj in resObject["data"]:
                    if (str(obj["id"]) == challenge[0][1]):
                        complete = complete + 1
            except Exception:
                total = total - 1
        await ctx.channel.send(
            f'{complete} / {total} or {int(100 * (complete / total))}% have completed the challenge so far!!')


def setup(client):
    client.add_cog(CodeWars(client))
