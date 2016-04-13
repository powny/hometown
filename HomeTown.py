import urllib
from BeautifulSoup import *
import win_unicode_console 
win_unicode_console.enable()
import xml.etree.ElementTree as ET
import sqlite3
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pprint

conn = sqlite3.connect('hometown.sqlite')
cur = conn.cursor()
cur.executescript('''

CREATE TABLE IF NOT EXISTS Homes ("Unique ID" TEXT UNIQUE, "Description" TEXT, Price TEXT, "Date added" TEXT, Link TEXT)''')

new_homes = 0
soupMail = BeautifulSoup(open('mail2.html'))
html = Tag(soupMail, "html")
table = Tag(soupMail, "table")
body = Tag(soupMail, "body")
tr = Tag(soupMail, "tr")
td = Tag(soupMail, "td")
soupMail.append(html)
html.append(body)
body.append(table)
table.append(tr)
table.attrs.append(("bgcolor", "purple"))
tr.append(td)

td.append('POWNY FOUND HOMES!')

td.attrs.append(('align', "center"))
td.attrs.append(('bgcolor', "NavajoWhite"))


url = 'http://www.daft.ie/galway-city/residential-property-for-rent/galway-city-centre,galway-city-suburbs/?s%5Bignored_agents%5D%5B0%5D=5732&s%5Bignored_agents%5D%5B1%5D=428&s%5Bignored_agents%5D%5B2%5D=1551&s%5Bsort_by%5D=date&s%5Bsort_type%5D=d&searchSource=rental'
home_count = 0
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

homes = soup.findAll('div', {'class' : 'box' })
for item in homes:
    home_date = item.find('div', { 'class' : 'date_entered' }).getText()
    #print home_date
    for image in item('img', {'class' : 'main_photo' }) :
        home_description = image.get('alt', ' ')
    for image in item('img', {'class' : 'main_photo lazy' }):
        home_description = image.get('alt', ' ')
    #print home_description
    home_price = item.find('strong', { 'class' : 'price' }).getText()
   # print home_price
    for image in item('img', {'class' : 'main_photo' }) :
        home_ID = image.get('id', ' ')
    for image in item('img', {'class' : 'main_photo lazy' }):
        home_ID = image.get('id', ' ')
    #print home_ID
    home_linker = item.find('a')
   # print 'http://www.daft.ie'+(home_linker['href'])
    home_link = 'http://www.daft.ie'+(home_linker['href'])

    
    try:
        print 'Home ID:', home_ID
        SQL_ID = home_ID
    except: 
        print 'Home description: Undisclosed'
        SQL_Desc = 'Undisclosed'
    try:
        print 'Home desription:', home_description
        SQL_Desc = home_description
    except: 
        print 'Home description: Undisclosed'
        SQL_Desc = 'Undisclosed'
    try:
        print 'Home link:', home_link
        SQL_Link = home_link
    except:
        print 'Home link: Unavailable'
        SQL_Link = 'Unavailable'
    try:
        print 'Home date:', home_date
        SQL_Date = home_date
    except:
        print 'Home date: Unavailable'
        SQL_Date = 'Unavailable'
    try:
        print 'Home price:', home_price, '\n'
        SQL_Price = home_price
    except:
        print 'Home price:: Unavailable', '\n'
        SQL_Price = 'Unavailable'
        home_list.append(SQL_Desc + 'for' + SQL_Price + 'Link:' + SQL_Link + '\n').encode('ascii', 'ignore')
        
    home_count = home_count + 1
    SQL_Date = time.strftime("%c")

    home_full = [SQL_Desc, SQL_Price, SQL_Link]
                        
    try:
        cur.execute('''INSERT INTO Homes ("Unique ID", "Description", "Price", "Date added", "Link") 
        VALUES ( ?, ? , ? , ?, ? )''', (SQL_ID, SQL_Desc, SQL_Price, SQL_Date, SQL_Link) )
        home_full = [SQL_Desc, SQL_Price, SQL_Link]
        td.append('<ul>')
        for attr in home_full:
            td.append(attr)
            td.append(' // ')
        td.append('</ul>')
        new_homes = new_homes + 1
    except: 
        continue   

mail_date = str(time.strftime("%x"))
addMailTitle = soupMail.findAll("title")
mail_count = str(new_homes)
for tag in addMailTitle:
    tag.insert(0, NavigableString(mail_count + ' new homes on ' + mail_date))
print(soupMail.prettify())
htmail = soupMail.prettify()
if new_homes > 0:
    msg = MIMEMultipart()
    fromaddr = 'your@gmail.com'
    toaddr = 'to@gmail.com'
    msg['From'] = 'your@gmail.com'
    msg['To']  = 'to@gmail.com'
    msg['Subject'] = mail_count + ' new homes on ' + mail_date
    msg.attach(MIMEText(htmail, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "yourPW")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()   
conn.commit()

