world-cup-texts
===============
import json
import sys
import urllib
from datetime import datetime
from twilio.rest import TwilioRestClient

url = "http://worldcup.sfg.io/matches/"
result = json.load(urllib.urlopen(url))

def local_time(t):
	parse_time = datetime.strptime(t[:len(t)-6], '%Y-%m-%dT%H:%M:%S.%f')
	time_change = -4 #Hours
	hour = parse_time.hour
	new_hour = hour + time_change
	if new_hour > 12: 
		new_hour = new_hour - 12
		am_or_pm = "PM"
	elif new_hour == 12:
		am_or_pm = "PM"
	else:	
		am_or_pm = "AM"
	hour_print = str(new_hour) + ":00 " + am_or_pm
	return hour_print

def month_text(mon):
	if mon == 1: return "January"
	if mon == 2: return "February"
	if mon == 3: return "March"
	if mon == 4: return "April"
	if mon == 5: return "May"
	if mon == 6: return "June"
	if mon == 7: return "July"
	if mon == 8: return "August"
	if mon == 9: return "September"
	if mon == 10: return "October"
	if mon == 11: return "November"
	if mon == 12: return "December"

# Initialize
#-------------------------------------------------------------------------
today_day = datetime.now().day
today_month = datetime.now().month
today_msg = month_text(today_month) +" " + str(today_day) + " Games:\n "
tom_msg = "\n Tomorrow's Games: \n"
output_today = today_msg
output_tomorrow = tom_msg

# Main
#-------------------------------------------------------------------------
for i in result:
	game_time = i["datetime"]
	start_time = local_time(game_time)
	parsed_date = datetime.strptime(game_time[:len(game_time)-6], '%Y-%m-%dT%H:%M:%S.%f')
	game_month = parsed_date.month
	game_day = parsed_date.day
	if today_month == game_month:
		#Today's Games
		if  game_day - today_day == 0:
			home_team =  str(i["home_team"]["country"])
			home_goals =  str(i["home_team"]["goals"])
			away_team =  str(i["away_team"]["country"])
			away_goals =  str(i["away_team"]["goals"])
			game = home_team +  " vs. " + away_team + ": " + start_time + '\n' + home_goals + " - " + away_goals + '\n' 
			output_today += game
		#Tomorrow's Games
		elif game_day - today_day == 1:	
			home_team =  str(i["home_team"]["country"])
			away_team =  str(i["away_team"]["country"])
			game = home_team +  " vs. " + away_team + '\n' + start_time + '\n\n'
			output_tomorrow += game

# Text
#-------------------------------------------------------------------------
txt_body = output_today + output_tomorrow
# print txt_body

account_sid = "AC27cc2b3137a1bdc7b82931a9c9de3247"
auth_token  = "c6f315ed2510eb1bfad8e31351237481"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body= txt_body,
    to="+13142294506",
    from_="+13146674285")
print message.sid,  '\n Message Sent!'
