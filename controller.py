
class Controller():
    def __init__(self, rc):
        self.rc = rc
        self.commonds = {
            'h': self.help,
            'status': self.status,
            'stop': self.stop,
        }
    
    def execute_command(self, cmd, client_address=''):
        cmd_split = cmd.strip().split(' ')
        if cmd_split[0] in self.commonds:
            return self.commonds[cmd](cmd_split)
        else:
            return 'unknown commonds %s' % cmd
    
    def help(self, cmd_split):
        rsp = ''
        for available_cmd in self.commonds:
            rsp += '%s\n' % available_cmd
        return rsp
    
    def status(self, cmd_split):
        rsp = 'TODO: finish status cmd'
        return rsp

    def stop(self, cmd_split):
        self.rc.main_server.stop()
        return ''