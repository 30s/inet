from cmd import Cmd

from weibo import APIClient

from settings_ax003d import APP_KEY, APP_SECRET, CALLBACK_URL, TOKEN


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

    def do_timeline(self, line):
        timeline = self.client.statuses.user_timeline.get()
        for s in timeline.statuses:
            print 80 * '*'
            print s.created_at
            print s.user.screen_name
            print s.text
            print s.source


if __name__=='__main__':
    inet = INet()
    inet.cmdloop()

