from libs.btpeer import *
import os
import hashlib
from datetime import datetime



#-------------------------------------------------------
# Message types
CHATMSG = "CHAT"
#-------------------------------------------------------

class DBMember(BTPeer):

    __candidates_and_votes = {}

    def __init__(self, maxpeers, serverport, myid=None):
        BTPeer.__init__(self, maxpeers, serverport, myid)

        self.files = {}  # available files: name --> peerid mapping
        self.addrouter(self.__router)
        self.hashed_id = hashlib.sha256(self.myid.encode()).hexdigest()
        self.contacts = {} # contacts of peer
        self.file_dir = self.__init_filepath()

        handlers = {
            CHATMSG : self.__handle_chatmsg
        }

        for mt in handlers:
            self.addhandler(mt, handlers[mt])


    def __debug(self, msg):
        if self.debug:
            btdebug(msg)


    def __router(self, peerid):
        if peerid not in self.getpeerids():
            return (None, None, None)
        else:
            rt = [peerid]
            rt.extend(self.peers[peerid])
            return rt


    def __get_name(self, peerconn):
        keys_list = list(self.contacts.keys())
        val_list = list(self.contacts.values())
        if peerconn.id in val_list:
            pos = val_list.index(peerconn.id)
            peer_name = keys_list[pos]
        else:
            peer_name = peerconn.id
        return peer_name


    def __handle_chatmsg(self, peerconn, data):
        self.peerlock.acquire()
        try:
            peer_name = self.__get_name(peerconn)
            prefix = f'client[{peer_name}]'
            print('\r\r' + f'{prefix}: ' + data + '\n' + f'you: ', end='')
        finally:
            self.peerlock.release()


    def add_contact(self, name, host, port):
        peerid = host + ':' + str(port)
        self.addpeer(peerid=peerid, host=host, port=port)
        self.contacts[name] = peerid


    def send_to_contact(self, name, msg, type):
        self.sendtopeer(self.contacts[name], msgtype=type, msgdata=msg, waitreply=False)
        # TODO: I should consider making reply handlers
        # print(self.contacts[name])
        # print(self.peers[self.contacts[name]])


    def list_contacts(self):
        inc = 1
        for i in self.contacts.keys():
            print('%d: ' % inc + i)
            inc += 1


    def list_candidates(self):
        inc = 1
        for i in self.__candidates_and_votes.keys():
            votes = self.__candidates_and_votes[i]
            print(f'{inc}: {i} - {votes} votes')
            inc += 1


    # TODO: finish vote_for function
    def vote_for(self, candidate):
        if candidate in self.__candidates_and_votes.keys():
            file_name = os.path.join(self.file_dir, self.hashed_id + datetime.now().strftime('%H%M%S') + '.txt')
            with open(file_name, 'w') as f:
                f.write(candidate)
            self.__candidates_and_votes[candidate] += 1
        else:
            print('No such candidate with that name')


    def add_candidate(self, candidate):
        self.__candidates_and_votes[candidate] = 0


    def __init_filepath(self):
        cwd = os.getcwd()
        tfd = os.path.join(cwd, 'files', self.hashed_id)
        if not os.path.exists(tfd):
            os.mkdir(tfd)
        return tfd


    def start_loop(self, target): # listening for connections
        th = threading.Thread(target=target, daemon=True)
        th.start()
        return th
