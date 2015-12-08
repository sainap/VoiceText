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

import webapp2
import jinja2
from hw7 import flickrREST, get_photo_ids, get_photo_info, get_photo_url

import os
import logging

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
        vals = {}
        vals['title'] = "Talk App"
        vals['message'] = "Hello, today I would like to introduce to you the new generation for our websites, are you ready for this?"
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(vals))

class HelloHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        vals['page_title']="Hello page"
        logging.info(type(self))
        req = self.request
        logging.info(type(req))
        vals['url']= req.url
        ## for url paths that look like /hello.html?n=4&name=you
        n = int(req.get('n', 1))
        term = req.get('term', 'world')
        vals['greeting']="Hello " + term
        vals['counter_list']= range(n)
        template = JINJA_ENVIRONMENT.get_template('hello.html')
        self.response.write(template.render(vals))
      
        
class GreetHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        vals['page_title']="Talk App"
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(vals))

def greet_person(name, t):
    if t == "birthday":
        return "Happy Birthday this month,  %s!" % (name)
    else:
        return "Hello %s" % (name)

class GreetResponseHandler(webapp2.RequestHandler):
    def post(self):
        vals = {}
        vals['page_title']="Greeting Page Response"
        term = self.request.get('term')
        submit = self.request.get('submit') 
        logging.info(term)
        logging.info(submit)
        if term:
            pics = get_photo_url(term)
            for pic in pics:
                logging.info(pics[pic])
            if len(pics) == 0:
                vals['message'] = 'please try another search term, no gifs for this term found.'
            else:
                vals['pics'] = pics


            template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
            self.response.write(template.render(vals))
            logging.info('term= '+term)
        else:
            #if not, then show the form again with a correction to the user
            vals['prompt'] = "How can I greet you if you don't enter a term?"
            template = JINJA_ENVIRONMENT.get_template('greetform.html')
            self.response.write(template.render(vals))
    

# for all URLs except alt.html, use MainHandler
application = webapp2.WSGIApplication([ \
                                      ('/greetings', GreetHandler),
                                      ('/gresponse', GreetResponseHandler),
                                      ('/hello.html', HelloHandler),
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)
