import cmd


class INetManager(cmd.Cmd):
    def init(self):
        cmd.Cmd.init(self)

    def help_wb_new(self):
        print "new weibo messages"

    def do_wb_new(self, line):
        print "new weibo"	


if __name__=='__main__':
    inet = INetManager()
    inet.cmdloop()

