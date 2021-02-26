#!/usr/bin/env python # -*- coding: utf-8 -*-

import sys, argparse, time, subprocess, shlex, logging, os, re

from bigbluebutton_api_python import BigBlueButton, exception
from bigbluebutton_api_python import util as bbbUtil 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import get_meeting 

from datetime import datetime

downloadProcess = None
browser = None
selenium_timeout = 30
connect_timeout = 5

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

bbb = BigBlueButton(get_meeting.server, get_meeting.secret)
bbbUB = bbbUtil.UrlBuilder(get_meeting.server, get_meeting.secret)
      
      
def get_join_url(params):
	params = params
	try:
		params = params.split(" ")
		joinParams = {}
		joinParams['meetingID'] = params[0]
		joinParams['fullName'] = params[1]
		joinParams['password'] = params[2]
		# joinParams['userdata-bbb_auto_join_audio'] = "true" 
		# joinParams['userdata-bbb_enable_video'] = 'false' 
		# joinParams['userdata-bbb_listen_only_mode'] = "false" 
		# joinParams['userdata-bbb_force_listen_only'] = "false" 
		# joinParams['userdata-bbb_skip_check_audio'] = 'false' 
		joinParams['joinViaHtml5'] = 'true'
		return bbbUB.buildUrl("join", params=joinParams) 
	except:
		logging.info("No Meeting")

def create_join_url(id):
    meeting_url = get_join_url(get_meeting.url_param(id))
    return recorder_(meeting_url,id)
    
def recorder_(meeting_url,id):
    meeting_url = meeting_url
    id = id
    params = get_meeting.url_param(id)
    try:
        params = params.split(" ")
        bot_join = 'node liveJoin.js ' + meeting_url + ' ' + params[3] + '.webm'
        bot_args = shlex.split(bot_join)
        # return subprocess.Popen(bot_args)
        return bot_args
    except:
        logging.info("No Meeting url")
# current date and time
now = datetime.now()
fileTimeStamp = now.strftime("%Y%m%d%H%M%S")
idlist = get_meeting.bbb_record_join(bbbUB.bbbServerBaseUrl)
print(idlist)
for id in idlist:
    print(create_join_url(id))
    