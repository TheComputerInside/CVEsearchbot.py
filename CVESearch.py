import discord
import feedparser
import urllib.request
from pycvesearch import CVESearch
from shodan import Shodan
import os
import shodan.helpers as helpers
import sys
import base64
import json


# The Computer Inside presents:
# The CVESearch.py discord bot!
#      (name not final)
#
# Please read the documentation
# before continuing.(use [~docs]!)


#minimum and maximum screenshots we
#want shodan to send
MIN_SCREENS = 1
MAX_SCREENS = 1

#manual version numbers
vernum= "0.13.1"
branch = "current-stable"


#library declarations
client = discord.Client()
cve = CVESearch()



#tokens! Put your API keys here. For discord, make sure you go to your
#devpage (https://discordapp.com/developers/applications/) to get your key
shodan = Shodan('')
TOKEN = 'Discord token!'
        
#help tooltips (it's easier not to ask)

usagetitle = "Usage:"
feedtt = "~feed, ~feed2, ~feed3"
feedhelp = "Gets the most recent CVEs from the feed"
cvesrchtt = "~cvesearch CVE-YEAR-###### \n Searches for and displays the specified CVE. You must use the CVE ID format when using this command to avoid errors."
cvesrchhelp = "Searches for and displays the specified CVE"
metasploittt = "~metasploit CVE-YEAR-###### \n Gets the metasploit module for the specified CVE, if any"
metasploithelp = "Gets the metasploit module for the specified CVE, if any"
shodansrchtt = "~shodan-search filter:\"param\""
shodansrchhelp = "Gets information for a random machine on Shodan. Also sends a screenshot if the entry has one. Based on parameters"
shodansfhelp = "Gets a screenshot for a random machine on shodan based on parameters"
shodansftt = "~shodansafari filter:\"param\" \n See the documentation for a more detailed overview."
helptt = "~help [command(optional)]"
helphelp = "shows the help dialog. If a command is specified, the tooltip for the command is shown instead"
docstt = "~docs"
docshelp = "Shows the official(tm) documentation"
exploitdbtt = "~exploitdb CVE-YEAR-###### \n Finds and posts the exploit-db entry for the specified vulnerability."
exploitdbhelp = "Shows the exploit-db entry for the specified CVE, if any"
shdtokenstt = "~shdtokens \n Shows how many Shodan query credits you have left. \n Credits regenerate each month."
shdtokenshelp = "Shows how many Shodan query credits you have left. \n Credits regenerate each month."



#giving some notification that the discord bot is ready 
@client.event
async def on_ready():
    print("////rdy!!////")
    
    

@client.event
async def on_message(message):
    #wow look at that! This is where the feed comes from
    d=feedparser.parse('https://www.cvedetails.com/vulnerability-feed.php')
    
    #make it so the bot doesn't reply to itself 
    if message.author == client.user:
        return

    #Explanation about these:
    #These are like this since discord decided to add
    #a 2000 char limit to all messages. If unhandled,
    #it will return a fake 400 error which just means
    #that it went over. Attempts to try and fit more than
    #3-4 entries per command have all but failed.

    #This is why I implemented the try and except statements.
    #If four is too much, it'll just cut it down to three.
    if message.content == "~feed":
        #these look kinda gross, but you should have seen
        #the original code. This is crystal compared
        #to the garbage in v0.1
        embed2=discord.Embed()
        embed2.add_field(name=d.entries[0].title, value=d.entries[0].description, inline=False)
        embed2.add_field(name=d.entries[1].title, value=d.entries[1].description, inline=False)
        embed2.add_field(name=d.entries[2].title, value=d.entries[2].description, inline=False)
        embed2.add_field(name=d.entries[3].title, value=d.entries[3].description, inline=False)
        try:
            await message.channel.send(content=None, embed=embed2)
        except:
            embed3=discord.Embed()
            embed3.add_field(name=d.entries[0].title, value=d.entries[0].description, inline=False)
            embed3.add_field(name=d.entries[1].title, value=d.entries[1].description, inline=False)
            embed3.add_field(name=d.entries[2].title, value=d.entries[2].description, inline=False)
            await message.channel.send(content=None, embed=embed3)
            
    if message.content == "~feed2":
        
        embed=discord.Embed()
        embed.add_field(name=d.entries[8].title, value=d.entries[6].description, inline=False)
        embed.add_field(name=d.entries[9].title, value=d.entries[7].description, inline=False)
        embed.add_field(name=d.entries[10].title, value=d.entries[8].description, inline=False)
        embed.add_field(name=d.entries[11].title, value=d.entries[9].description, inline=False)
        try:
            await message.channel.send(content=None, embed=embed)
        except:
            embed=discord.Embed()
            embed.add_field(name=d.entries[8].title, value=d.entries[6].description, inline=False)
            embed.add_field(name=d.entries[9].title, value=d.entries[7].description, inline=False)
            embed.add_field(name=d.entries[10].title, value=d.entries[8].description, inline=False)


    if message.content.startswith ("~cvesearch"):
        embed=discord.Embed()
        text = message.content
        prefix = "~cvesearch "
        print(message.content)
        #this is how we remove the command so we
        #can actually search for the vulns we
        #want
        text = text.replace(prefix, "", 1)
        print(text)
        #the CVESearch lib is incredibly helpful
        #for this. Whilst bare-bones, I don't actually
        #have to parse JSON unless I want to get more
        #from the API itself. 
        var4 = cve.id(text)
        var5 = var4.get('summary')
        print(var5)
        embed.add_field(name=text, value=var5, inline=False)
        
        await message.channel.send(content=None, embed=embed)
                    
    if message.content.startswith ("~help"):
        text = message.content
        prefix = "~help "
        text = text.replace(prefix, "", 1)
        #debug
        print(text)
        
        # EDIT: Help is kinda broken now, but
        # The good news is that there is 
        # now just cleaner code as a result.
        # You may want to reference the docs
        # until I get a file together for
        # the help entries. It was 0630
        # when I wrote this after a long night.
        helpembed=discord.Embed(color=0xffc20d)
        helpfile = open('tooltips.txt', 'r')
        helpdict = json.loads(helpfile.read())
        #debug, but I've commented this out since
        # it gets annoying really fast
        # print(helpdict)
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
        #is that an actual color? It is!
        #it looks so pretty now!
        embed=discord.Embed(color=0x4f4fff)
        text = message.content
        #I should probably be using a string literal
        #for this.
        prefix = "~metasploit "
        print(message.content)
        text = text.replace(prefix, "", 1)
        print(text)
        var4 = cve.id(text)
        #This is pretty gross as well, but
        #as it turns out, metasploit
        #entries can *also* become quite
        #long-winded. Discord hates this
        #and returns 400s because it's
        #discord and they don't care about
        #your problems with their API
        
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
        #Here are the official docs, if you want to flip through them
        embed=discord.Embed(title="Official(™) Documentation", url="https://github.com/TheComputerInside/CVEsearchbot.py/wiki", description="Contains commands, Shodan filters, and the changelog.", color=0x008000)
        await message.channel.send(content=None, embed=embed)

    if message.content.startswith ("~shodan-search"):
        #ah yes. My favorite feature so far.
        #I've made a mistake in assuming that you
        #just want entries with screenshots
        #so sometimes the code will fail
        #if you try and get like an ssh server
        #or something. This is high priority
        #and I plan on getting it out ASAP
        tokenmsg = "Tokens Left:"
        sdinfobuffer0 = shodan.info()
        tokensleft = sdinfobuffer0.get('query_credits')
        if tokensleft > 0:
            
            embed=discord.Embed(color=0xff097d)
            embed.set_footer(text="Powered by the Shodan API. Thanks Shodan!")
            text = message.content
            prefix = "~shodan-search "
            text = text.replace(prefix, "", 1)
            try:
                #ew.
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
                    #so this is pretty disgusting, but
                    #required as well.
                    #Screenshots in the shodan API
                    #are encoded in base64, so we
                    #have to dump those to disk
                    #before sending them off
                    #to discord.
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
        #this is literally copy-pasted from the previous
        #entry. I just wanted to get the screenshot :'(
        tokenmsg = "Tokens Left:"
        sdinfobuffer1 = shodan.info()
        tokensleft = sdinfobuffer1.get('query_credits')
        if tokensleft > 0:
            embed=discord.Embed(color=0xff097d)
            params0 = message.content
            prefix = "~shodansafari"
            params0 = params0.replace(prefix, "")
            #interestingly, Shodan's API doesn't seem to
            #care about having an extra space in front
            #of the filters. How odd.
            params0 = "has_screenshot:\"true\"" + params0
            print(params0)
            searchdict =  shodan.search(params0,page=1,limit=1,minify=False)
            searchbuffer0 = searchdict.get('matches')
            print(tokensleft)
            try:
                optsimage = searchbuffer0[0].get('opts')
                screenimage = optsimage.get('screenshot')
                imagedata = screenimage.get('data')
                #we have to export it as unicode since
                #that's exactly what it is.
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
	#I bet this looks like another routine,
        #huh? It's the metasploit entry except stripped down
        #to accomodate the bits of information exploit-db
        #has in the CVESearch entry. Eventually I'd
        #like to get more, but this will do for now.
        print(message.content)
        msgbuffer = msgbuffer.replace(prefix, "", 1)
	#debugging print statement
        print(msgbuffer)
        #I would NOT recommend my variable naming scheme
        #I will be fixing that within the next few patches.
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
            #Custom error message. Yet another thing I have to optimize.
            error1 = "Vulnerability contains no exploit-db entry"
            embed.add_field(name=error0, value=error1, inline=False)
        try:
            await message.channel.send(content=None, embed=embed)
        except:
            #oh look, Discord! Error handling just for you!
            #I get the char limit thing, but seriously. 
            embed1=discord.Embed(color=0x4f4fff)
            errortitle0 = "Discord Error"
            errordesc0 = "Message breaches char limits."
            errortitle1 = "Please use this link to the CVE entry instead:"
            errordesc1 = "https://cve.circl.lu/cve/" + text
            embed1.add_field(name=errortitle0, value=errordesc0, inline=False)
            embed1.add_field(name=errortitle1, value=errordesc1, inline=False)
            await message.channel.send(content=None, embed=embed1)
            
    if message.content.startswith ("~shdtokens"):
        # Getting the tokens is a bit slow. I think I'm going to implement
        # a little 'hold on' message that gets deleted after a few seconds.
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
        #the RDM's favorite block of code.
        #all joking aside, this just gets version information
        #stored in a string. I'm trying to think of better methods, but
        #I digress. 
        verembed=discord.Embed(color=0x3eb715)
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

    

#Running the discord bot        
client.run(TOKEN)
