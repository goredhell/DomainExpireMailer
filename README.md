# DomainExpireMailer
Checks domains expire dates and send an e-mail about it

You should install module whois first
 * pip install python-whois *

Also you need to create a txt file "C:\DomainList\domains.txt" enter a domain for each line

Things you need to change for sending mail : 

- SENDER_MAIL_ADDRESS : Mail address for sending the mail
- PASSWORD : Mail addresses smtp password
- STMP_SERVER_ADDRESS : smtp address for sending mail
- SMTP_PORT : Port for sending mail
- RECEIVE_MAIL_ADDRESS : Mail address to receive mails
