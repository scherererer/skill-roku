# The MIT License (MIT)
#
# Copyright (c) 2018 Michael P. Scherer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import urllib.request

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

class RokuSkill(MycroftSkill):

	# The constructor of the skill, which calls MycroftSkill's constructor
	def __init__(self):
		super(RokuSkill, self).__init__(name="RokuSkill")

		self.ssdpQuery =
			'M-SEARCH * HTTP/1.1\nHost: 239.255.255.250:1900\nMan: "ssdp:discover"\nST: roku:ecp\n\n'

	def get_intro_message (self):
		return self.translate("intro")

	# The "handle_xxxx_intent" function is triggered by Mycroft when the
	# skill's intent is matched.  The intent is defined by the IntentBuilder()
	# pieces, and is triggered when the user's utterance matches the pattern
	# defined by the keywords.  In this case, the match occurs when one word
	# is found from each of the files:
	#    vocab/en-us/Hello.voc
	#    vocab/en-us/World.voc
	# In this example that means it would match on utterances like:
	#   'Hello world'
	#   'Howdy you great big world'
	#   'Greetings planet earth'
	@intent_handler(IntentBuilder("").require("Show").require("Source"))
	def handle_roku_show_intent(self, message):
		# In this case, respond by simply speaking a canned response.
		# Mycroft will randomly speak one of the lines from the file
		#    dialogs/en-us/hello.world.dialog

		# TODO: Discover this IP
		address = "192.168.10.20"

		provider = ""
		src = message.data["Source"]

		# TODO: A list of providers comes from http://<address>:8060/query/apps
		#  In the future, could query this at startup, and then dynamically add
		#  the available sources to the list of providers. For now, just hard coding
		#  some popular ones.
		if src == "netflix":
			provider = "12"
		elif src == "amazon":
			provider = "13"
		elif src == "youtube":
			provider = "837"
		elif src == "tiny desk concerts":
			provider = "41305"
		elif src == "tune in" || src == "tunein":
			provider = "1453"
		elif src == "plex":
			provider = "13535"
		else:	# Roku
			provider = ""

		if provider != "":
			provider = "&provider-id=" + provider

		keyword=self._extract_show(message)

		url = 'http://{}:8060/search/browse?keyword={}{}&launch=true'.format (address, keyword.replace(" ", "%20"), provider)

		try:
			postdata = urllib.parse.urlencode({}).encode()
			req = urllib.request.urlopen(url, data=postdata)
		except:
			self.speak_dialog("failure")
			return;

		self.speak_dialog("playing", data={"show": keyword, "source": src})

	def _extract_show(self, message):
		utterance = message.data["utterance"]
		utterance = utterance.replace(message.data["Show"], "")
		utterance = utterance.replace(message.data["Source"], "")

		# strip out other non important words
		common_words = [" to ", " on ", " with ", " using "]

		for words in common_words:
			utterance = utterance.replace(words, "")

		return utterance.strip();

	# The "stop" method defines what Mycroft does when told to stop during
	# the skill's execution. In this case, since the skill's functionality
	# is extremely simple, there is no need to override it.  If you DO
	# need to implement stop, you should return True to indicate you handled
	# it.
	#
	# def stop(self):
	#    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
	return RokuSkill()
