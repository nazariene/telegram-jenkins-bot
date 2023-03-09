# telegram-jenkins-bot
Telegram bot to run Jenkins jobs


# Run
## Environment variables

Name | Description | Example 
--- | --- | --- 
TELEGRAM_TOKEN | Token for your telegrambot | 123123abcabc:123123abc
ALLOWED_USERS | List of users allowed to use your bot (their ids). If not set - everyone are allowed | 418770312,12312312  
JENKINS_URL | Url to jenkins | https://jenkins.yourdomain.com
JENKINS_USERNAME | Username to login to jenkins | John
JENKINS_PASSWORD | Jenkins password | 12345
## Console
export TELEGRAM_TOKEN=1111 JENKINS_URL=http://jenkins.com JENKINS_USERNAME=john JENKINS_PASSWORD=123 python3 jenkins-bot.py

## Docker
docker run -d -e TELEGRAM_TOKEN=1111 \
    -e JENKINS_URL=http://jenkins.com \
    -e JENKINS_USERNAME=john \
    -e JENKINS_PASSWORD=12345 \
    jenkins-telegram-bot 