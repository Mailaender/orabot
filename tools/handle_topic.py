# Copyright 2011-2014 orabot Developers
#
# This file is part of orabot, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import json

def start(self):
    while  True:
        time.sleep(3600)  # wait an hour
        change_topic(self)

def change_topic(self):
    url = 'https://api.github.com/repos/OpenRA/OpenRA/tags'
    try:
        stream = self.data_from_url(url, None)
    except Exception as e:
        print(("*** [%s] %s: %s") % (self.irc_host, __name__, e))
        return
    release = get_version(self, stream, 'release')
    playtest = get_version(self, stream, 'playtest')
    filename = 'var/version.txt'
    lines = []
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
    except:
        pass    # no file exists
    if ( lines == [] ):
        write_version(release, playtest)
        return
    if ( (release + '\n' not in lines) or (playtest + '\n' not in lines) ):
        if self.irc_host == "irc.freenode.net":
            topic = "[logged] open-source RTS | latest: %s | testing: %s | http://open-ra.org | http://bugs.open-ra.org" % (release, playtest)
            self.topic('#openra', topic)
            print("*** [%s] Attempt to change the TOPIC of #openra" % self.irc_host)
        elif self.irc_host == "irc.open-ra.org":
            topic = "Latest release: %s | Latest playtest: %s" % (release, playtest)
            self.topic('#global', topic)
            print("*** [%s] Attempt to change the TOPIC of #global" % self.irc_host)
        write_version(release, playtest)

def get_version(self, stream, version):
    result = ""
    y = json.loads(stream)
    for item in y:
        result = item['name'].split('-')[1]
        if item['name'].split('-')[0] == version:
            break
    return result

def write_version(release, playtest):
        filename = 'var/version.txt'
        file = open(filename, 'w')
        file.write(release + "\n" + playtest + "\n")
        file.close()
