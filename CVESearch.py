import discord
from pycvesearch import CVESearch
from shodan import Shodan
import base64
import json

# The Computer Inside presents:
# The CVESearch.py discord bot!
#      (name not final)
#
# Please read the documentation
# before continuing.(use [~docs]!)


# minimum and maximum screenshots we
# want shodan to send
MIN_SCREENS = 1
MAX_SCREENS = 1

# manual version numbers
vernum= "0.20"
branch = "current"


# library declarations
client = discord.Client()
cve = CVESearch()
shodan = Shodan('')




# discord bot token goes here
TOKEN = ''


#giving some notification that the discord bot is ready 
@client.event
async def on_ready():
    print("rdy!!")
    
    

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return


    if message.content.startswith ("~cvesearch"):
        embed=discord.Embed()
        text = message.content
        prefix = "~cvesearch "
        print(message.content)
        # this is how we remove the command so we
        # can actually search for the vulns we
        # want
        text = text.replace(prefix, "", 1)
        print(text)
        # the CVESearch lib is incredibly helpful
        # for this. Whilst bare-bones, I don't actually
        # have to parse JSON unless I want to get more
        # from the API itself.
        try:
            var4 = cve.id(text)
            var5 = var4.get('summary')
        except Exception as err:
            cveerrorembed=discord.Embed(title="cve.circl.lu error", description="an error has occured in getting details for the specified CVE.", color=0xff0000)
            cveerrorembed.set_footer(text=err)
            await message.channel.send(content=None, embed=cveerrorembed)

        try:            
            embed.add_field(name=text, value=var5, inline=False)
            
            await message.channel.send(content=None, embed=embed)
        except Exception as errthesequel:
            print("An error has occured (likely something to do with the CVE exception error handling firing?)")
            print("Ignoring, but please keep the following error around:")
            print(errthesequel)
                    
    if message.content.startswith ("~help"):
        text = message.content
        prefix = "~help "
        text = text.replace(prefix, "", 1)

        print(text)
        # because the prefix removal sometimes results
        # in an empty message, it seems like the replace-
        # ment doesn't always work. ~help should return a
        # list of commmands by itself now, and still cont
        # inue to work as it did back in v0.13.2.

        if text == "~help":
            text = "commands"
        print(text)

        helpembed=discord.Embed(color=0xffc20d)
        helpfile = open('tooltips.txt', 'r')
        helpdict = json.loads(helpfile.read())
        print(helpdict)
        try:
            helpdict_sent = helpdict.get(text)
        except:
            errortitle = "Error"
            error = "no command found. Please try again?"
            errorembed=discord.Embed()
            errorembed.add_field(name=errortitle, value=error, inline=False)
            await message.channel.send(content=None, embed=errorembed)
        else:
            helpembed.add_field(name=text, value=helpdict_sent, inline=False)
            await message.channel.send(content=None, embed=helpembed)
        
    if message.content.startswith ("~metasploit"):
        # As of version 0.12, all discord embeds will contain colours
        # to help spot differences between modules.
        embed=discord.Embed(color=0x4f4fff)
        text = message.content
        prefix = "~metasploit "
        print(message.content)
        text = text.replace(prefix, "", 1)
        print(text)
        var4 = cve.id(text)

        # As it turns out, metasploit
        # entries can *also* become quite
        # long-winded. Discord hates this
        # and returns 400s because it's
        # discord and they don't care about
        # your problems with their API.

        # Plan for v0.22: If the text
        # is too long for discord,
        # toss it to pastebin and drop
        # a link instead.
        
        try:
            var5 = var4.get('metasploit')
            desc = 'Description:'
            reli = 'Reliability'
            var6 = var5[1].get('id')
            var7 = var5[1].get('description')
            var8 = var5[1].get('reliability')
        
            embed.add_field(name=text, value=var6, inline=False)
            embed.add_field(name=desc, value=var7, inline=False)
            embed.add_field(name=reli, value=var8, inline=False)
        except:
            error0 = "Error"
            error1 = "Vulnerability contains no metasploit entry"
            embed.add_field(name=error0, value=error1, inline=False)
        try:
            await message.channel.send(content=None, embed=embed)
        except:
            embed1=discord.Embed(color=0x4f4fff)
            error2 = "Discord Error"
            error3 = "Message breaches char limits."
            error4 = "Please use this link to the CVE entry instead:"
            error5 = "https://cve.circl.lu/cve/" + text
            embed1.add_field(name=error2, value=error3, inline=False)
            embed1.add_field(name=error4, value=error5, inline=False)

            await message.channel.send(content=None, embed=embed1)

    if message.content == "~docs":

        embed=discord.Embed(title="Official(™) Documentation", url="https://github.com/TheComputerInside/CVEsearchbot.py/wiki", description="Contains commands, Shodan filters, and the changelog.", color=0x008000)
        await message.channel.send(content=None, embed=embed)

    if message.content.startswith ("~shodan "):

        tokenmsg = "Tokens Left:"
        sdinfobuffer0 = shodan.info()
        tokensleft = sdinfobuffer0.get('query_credits')
        if tokensleft > 0:
            
            embed=discord.Embed(color=0xff097d)
            embed.set_footer(text="Powered by the Shodan API. Thanks Shodan!")
            text = message.content
            prefix = "~shodan "
            text = text.replace(prefix, "", 1)
            try:
                # ew.
                searchdict =  shodan.search(text,page=1,limit=1,minify=False)
                searchbuffer0 = searchdict.get('matches')
                searchIP = searchbuffer0[0].get('ip_str')
                searchts = searchbuffer0[0].get('timestamp')
                searchinfo = searchbuffer0[0].get('data')
                searchproduct = searchbuffer0[0].get('product')
                ip = "IP address (No touchy!)"
                    
                print(tokensleft)
                timestamp = "Timestamp"
                embed.add_field(name=ip, value=searchIP, inline=True)
                embed.add_field(name=timestamp, value=searchts, inline=True)
                embed.add_field(name=searchproduct, value=searchinfo, inline=True)
                embed.add_field(name=tokenmsg, value=tokensleft, inline=False)
                try:
                    # Screenshots in the shodan API
                    # are encoded in base64 as a blob,
                    # so we have to dump those
                    # to disk before sending them
                    # off to discord.
                    image0 = searchbuffer0[0].get('opts')
                    image1 = image0.get('screenshot')
                    image2 = image1.get('data')
                    image3 = bytes(image2, 'utf-8')
                    with open("screenshot.png", "wb") as fh:
                        fh.write(base64.decodebytes(image3))
                    
                except:
                    print("no screenshot")
                else:
                    await message.channel.send(file=discord.File('screenshot.png'))
            except:
                error = "Error"
                error2 = "No results returned"
                embed.add_field(name=ip, value=searchIP, inline=True)
                await message.channel.send(content=None, embed=embed)
            else:
                await message.channel.send(content=None, embed=embed)
        else:
            errortitle = "Error:"
            errormsg = "You don't have any search tokens left!"
            embed.add_field(name=errortitle, value=errormsg, inline=True)
            await message.channel.send(content=None, embed=embed)

    if message.content.startswith ("~shodansafari"):
        tokenmsg = "Tokens Left:"
        sdinfobuffer1 = shodan.info()
        tokensleft = sdinfobuffer1.get('query_credits')
        if tokensleft > 0:
            embed=discord.Embed(color=0xff097d)
            params0 = message.content
            prefix = "~shodansafari"
            params0 = params0.replace(prefix, "")
            # interestingly, Shodan's API doesn't seem to
            # care about having an extra space in front
            # of the filters. How odd.
            params0 = "has_screenshot:\"true\"" + params0
            print(params0)
            searchdict =  shodan.search(params0,page=1,limit=1,minify=False)
            searchbuffer0 = searchdict.get('matches')
            print(tokensleft)
            try:
                optsimage = searchbuffer0[0].get('opts')
                screenimage = optsimage.get('screenshot')
                imagedata = screenimage.get('data')
                # we have to export it as unicode since
                # that's exactly what it is.
                imagedatadecode = bytes(imagedata, 'utf-8')
                with open("screenshot_shodan1.png", "wb") as fh:
                    fh.write(base64.decodebytes(imagedatadecode))
                await message.channel.send(file=discord.File('screenshot_shodan1.png'))
                    
            except:
                error = "Error"
                error2 = "No results returned"
                embed.add_field(name=error, value=error2, inline=True)
                embed.set_footer(text="Powered by the Shodan API. Thanks Shodan!")
                await message.channel.send(content=None, embed=embed)
        else:
            errortitle = "Error:"
            errormsg = "You don't have any search tokens left!"
            embed.set_footer(text="Powered by the Shodan API. Thanks Shodan!")
            embed.add_field(name=errortitle, value=errormsg, inline=True)
            await message.channel.send(content=None, embed=embed)

    if message.content.startswith ("~exploitdb"):
        embed=discord.Embed(color=0xff4d00)
        msgbuffer = message.content
        prefix = "~exploitdb "
        print(message.content)
        msgbuffer = msgbuffer.replace(prefix, "", 1)
        # debugging print statement
        print(msgbuffer)
        # I would NOT recommend my variable naming scheme
        # I will be fixing that within the next few patches.
        cvedictbuffer = cve.id(text)
        try:
            cvedictsource = cvedictbuffer.get('exploit-db')
            file = 'File:'
            src = 'Source:'
            title = 'Title:'  
            cvefile = cvedictsource[1].get('file')
            cvesrc = cvedictsource[1].get('source')
            cvetitle = cvedictsource[1].get('title')
            embed.add_field(name=title, value=cvetitle, inline=False)
            embed.add_field(name=src, value=cvesrc, inline=False)
            embed.add_field(name=file, value=cvetitle, inline=False)
        except:
            error0 = "Error"
            # Custom error message. Yet another thing I have to optimize.
            error1 = "Vulnerability contains no exploit-db entry"
            embed.add_field(name=error0, value=error1, inline=False)
        try:
            await message.channel.send(content=None, embed=embed)
        except:
            # oh look, Discord! Error handling just for you!
            # I get the char limit thing, but seriously.
            embed1=discord.Embed(color=0x4f4fff)
            errortitle0 = "Discord Error"
            errordesc0 = "Message breaches char limits."
            errortitle1 = "Please use this link to the CVE entry instead:"
            errordesc1 = "https://cve.circl.lu/cve/" + text
            embed1.add_field(name=errortitle0, value=errordesc0, inline=False)
            embed1.add_field(name=errortitle1, value=errordesc1, inline=False)
            await message.channel.send(content=None, embed=embed1)
            
    if message.content.startswith ("~shdtokens"):
        shdtkembed=discord.Embed(color=0xff097d)
        tokenmsg = "Tokens Left:"
        sdinfobuffer2 = shodan.info()
        tokensleft = sdinfobuffer2.get('query_credits')
        shdtkembed.add_field(name=tokenmsg, value=tokensleft, inline=False)
        shdtkembed.set_footer(text="Powered by the Shodan API. Thanks Shodan!")
        await message.channel.send(content=None, embed=shdtkembed)

    if message.content == "~version":
        versionstr = "Version"
        branchstr = "Branch"
        verembed=discord.Embed(color=0x008000)
        verembed.add_field(name=versionstr, value=vernum, inline=True)
        verembed.add_field(name=branchstr, value=branch, inline=True)
        await message.channel.send(content=None, embed=verembed)

    if message.content.startswith ("~msbulletin"):
        msgbuffer = message.content
        prefix = "~msbulletin "
        msgbuffer = msgbuffer.replace(prefix, "", 1)
        print(msgbuffer)
        try:
            msembed=discord.Embed(color=0x00d910)
            msbuffer0 = cve.id(msgbuffer)
            msbuffer1 = msbuffer0.get('msbulletin')
            print(msbuffer1)
            msdesc = msbuffer1[0].get('title')
            print(msdesc)
            msid = msbuffer1[0].get('bulletin_id')
            print(msid)
            msurl = msbuffer1[0].get('bulletin_url')
            print(msurl)
            msurl1 = msbuffer1[0].get('knowledgebase_url')
            print(msurl1)
            msknid = msbuffer1[0].get('knowledgebase_id')
            print(msknid)
            msembed.add_field(name=msid, value=msdesc, inline=True)
            msembed.add_field(name=msknid, value=msurl1, inline=True)
            msembed.set_footer(text=msurl)

            await message.channel.send(content=None, embed=msembed)
        except:
            msembed=discord.Embed(color=0x00d910)
            mserrortitle = "Error"
            mserror = "CVE entry contains no msbulletin information"
            msembed.add_field(name=mserrortitle, value=mserror, inline=True)
            await message.channel.send(content=None, embed=msembed)



# Running the discord bot
client.run(TOKEN)
