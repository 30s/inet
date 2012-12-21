import os

from cmd import Cmd
from datetime import datetime, timedelta

from weibo import APIClient


def print_status(s):
    if s.has_key('deleted') and s.deleted == u'1':
        return
    print 80 * '*'
    print s.idstr
    print s.created_at
    print s.user.screen_name
    print s.text
    print s.source    
    

class INet(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.client = APIClient(
            app_key=APP_KEY, 
            app_secret=APP_SECRET, 
            redirect_uri=CALLBACK_URL)

    def do_quit(self, line):
        exit(0)
    
    def do_login(self, line):
        url = self.client.get_authorize_url()
        print "Go to authorize in web browser:", url
        code = raw_input('code: ')
        r = self.client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        print r
        self.client.set_access_token(access_token, expires_in)

    def do_tlogin(self, line):
        r = TOKEN
        access_token = r['access_token']
        expires_in = r['expires_in']
        self.client.set_access_token(access_token, expires_in)

    def do_tl(self, line):
        self.do_timeline(line)

    def do_timeline(self, line):
        timeline = self.client.statuses.user_timeline.get()
        for s in timeline.statuses:
            print_status(s)

    def do_ft(self, line):
        self.do_friends_timeline(line)

    def do_friends_timeline(self, line):
        now = datetime.now()
        end, cur, max_id, timeline = now, None, None, None
        if line != '':
            end = now - timedelta(hours=int(line))
        while True:
            if max_id is None:
                timeline = self.client.statuses.friends_timeline.get()
            else:
                timeline = self.client.statuses.friends_timeline.get(
                    max_id=max_id)
            for s in timeline.statuses:
                print_status(s)
                cur = datetime.strptime(s.created_at, 
                                        '%a %b %d %H:%M:%S +0800 %Y')
                max_id = s.idstr
            if cur < end:
                break
                
    def do_fav(self, line):
        self.do_favorites(line)

    def do_favorites(self, line):
        resp = self.client.favorites.get()
        for f in resp.favorites:
            print_status(f.status)

    def do_destroy_favorite(self, line):
        resp = self.client.favorites.destroy.post(id=int(line))        

    def do_dfav(self, line):
        self.do_destroy_favorite(line)

    def help_favtags(self):
        print "tags for favorites"

    def do_favtags(self, line):
        resp = self.client.favorites.tags.get()
        for t in resp.tags:
            print ":".join([str(t.id), t.tag, str(t.count)])

    def do_tags(self, line):
        resp = self.client.tags.get(uid=TOKEN['uid'])
        print resp

    def do_unread(self, line):
        resp = self.client.remind.unread_count.get(uid=TOKEN['uid'])
        print resp

    def do_trends(self, line):
        resp = self.client.trends.get(uid=TOKEN['uid'])
        for t in resp:
            print t.trend_id, ":", t.hotword


if __name__=='__main__':
    import sys
    import getopt
    settings = "settings"
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', 'settings=')
        for opt, arg in opts:
            if opt in ["--settings"]:
                settings = arg
    except getopt.GetoptError:
        print "usage"
    exec "from %s import APP_KEY, APP_SECRET, CALLBACK_URL, TOKEN" % settings
    inet = INet()
    inet.cmdloop()

