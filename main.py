from libs.dbmember import *
import libs.extensions as ex

if __name__ == "__main__":
    mypeer = DBMember(0, 8080) # initializing server socket

    listen_thread = mypeer.start_loop(mypeer.mainloop) # starting listening loop

    ex.start_messaging(mypeer) # loop for sending messages and executing commands
