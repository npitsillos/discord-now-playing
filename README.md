# Discord Now Playing

A simple program to read what game you are playing by getting the details from Discord.

## How to Use
1. Fork this repository
2. Create a bot in Discord and invite it to your server
3. Create a `.env` file and add the following `TOKEN=<DISCORD_TOKEN>` `USERNAME=<DISCORD_USERNAME>`
4. You also need to launch an EC2 instance on AWS (a bit overkill so I need to find a better way)
5. Add the EC2 instance key, your token and username as secrets in your repository.

**Now Playing**

<img src=http://127.0.0.1:8000/ width="256" height="64" alt="Now Playing">