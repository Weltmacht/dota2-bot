# dota2-bot
### DOTA2 Discord Announcement Bot

```shell
git clone <repository name>
git status
git log
git add <files> 
git commit -m 'updated README.md'
git push -u origin main
```

1. Setup VSCode
    1. Install VSCode
    1. Install Python 3.13(or higher)
    1. Install Git SCM & Git History Extension
    1. Install Python, Python Debugger, PyLance
1. Install Draw.IO https://drawio.com or https://draw.io (browser version)
1. Build Python virtual environment `python -m venv env`
    * Make sure to `./env/Scripts/activate.bat` to activate environment before installing or executing!
1. `pip install -r requirements.yaml` to install packages

If you do add any more packages, make sure to update the requirements file. `pip freeze > requirements.yaml`

TODO:
* ~~Find out how to get DOTA2 match start events to either call to Python, or find a way to subscribe to player starting a match  -- Game State Integration addon for DOTA2~~
* ~~How do we receive the request and respond or process properly~~
* Determine what data we want to collect to announce.
* Figure out how to get a parse queued and ran
* Find out what events will trigger an announce
* How to send messages to Discord channel