#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# import httplib2
import webapp2
import jinja2
import sys

sys.path.insert(0, 'libs')

from twilio.rest import TwilioRestClient

import os
import logging


# To find these visit https://www.twilio.com/user/account
account_sid = "AC2d4a9a06d880759331af9c996522e039"
auth_token  = "79f07659e30050dcaeb99b7ca397f5d4"

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
        vals = {}
        vals['page_title'] = "VoiceText"
        vals['message'] = "Hello, today I would like to introduce to you the new generation for our websites, are you ready for this?"
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(vals))

class ContactHandler(webapp2.RequestHandler):
    def post(self):
        req = self.request
        posted = False
        contacts = {"Tori Lee": "+12068546608", "Brandon K": "+14158572848", "Michael Beach": "+14155059279"}
        sequence = str(req.get('sequence'))
        if (len(sequence) > 0):
            desired_contact = ""
            for contact in contacts:
                firstname = contact.split()[0].lower()
                if firstname in sequence.lower():
                    logging.info("submitted contact as " + firstname)
                    desired_contact = contact
                    logging.info('~~~~~~~~~~~~~~~~~~~~~' + desired_contact)


            # calling doesn't work with twilio basic account            
            # if (sequence.startswith('call')):
            #     client = TwilioRestClient(account_sid, auth_token)
            #     call = client.calls.create(to="+14085551234",  # Any phone number
            #         from_="+12512167247", # Must be a valid Twilio number
            #         url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
            #     print call.sid

            if (sequence.startswith('text') and posted == False and len(desired_contact) > 2):
                text = sequence.split(desired_contact.split()[0],1)[1]
                client = TwilioRestClient(account_sid, auth_token)
                logging.info("tried to text")
                message = client.sms.messages.create(to=contacts[desired_contact], from_="+12512167247",
                    body=text)
                posted = True


    def get(self):
        vals = {}
        vals['page_title']="My Contacts"
        logging.info(type(self))
        req = self.request
        logging.info(type(req))
        vals['contacts']= {"Tori Lee": 2068546608, "Brandon K": 2068492019, "Michael Beach": 4155059279}
        n = int(req.get('n', 1))
        term = req.get('term', 'world')

        template = JINJA_ENVIRONMENT.get_template('contacts.html')
        self.response.write(template.render(vals))
      
        


    

# for all URLs except alt.html, use MainHandler
application = webapp2.WSGIApplication([ \
                                      ('/contactList', ContactHandler),
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)
