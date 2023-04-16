# FICSIT Assistant
Bot to assist with starting and stopping a Google Cloud Compute VM that runs the Satisfactory Dedicated Server.  Makes it easy for anyone to stop the VM when not in use to avoid unnecessary charges.

## Set-up
1.  Set up a Compute Engine VM that meets the requirements for the Satisfactory Dedicated Server in Google Cloud.
2.  Have the VM run the Satisfactory Server as a `systemd` service so that it automatically starts on boot.
3.  Set up a service account for that VM and give it the `Compute Instance Admin (v1)` and `Service Account User` roles.  Download the JSON key file (keep it secret) and save it as `key-file.json`.
4.  Take note of the `project_id`, `zone`, and `vm_name` in GCP and change those values accordingly in `server_bot.py`.
5.  Create a Discord application (bot) using the Discord Developer Portal and give it permissions to view and post messages.  Also make sure that the `Message Content Intent` setting is enabled.
6.  Take note of the API Key for the Discord bot and save it as a local environment variable called `SatisfactoryBotAPIKey`.
7.  Invite the bot your server and then run `server_bot.py` from your computer or a separate cloud-hosted computer.  (Can't use the same one since it'll get turned on and off by the bot)
8.  Enjoy!
