from libs.dbmember import *

COMMANDS = (
    "/help",
    "/addcontact",
    "/sendto",
    "/contacts",
    "/votefor",
    "/candidates",
    "/exit"
)

def start_messaging(peer: DBMember):
    peer.add_candidate("John")
    peer.add_candidate("Alice")

    while True:
        msg = input(f'you: ')

        list = msg.split(' ')
        command = list[0]

        if command in COMMANDS:
            if command == "/help":
                print(f'List of commands:')
                for i in COMMANDS:
                    print(i)
            elif command == "/addcontact":
                peer.add_contact(name=list[1], host=list[2], port=list[3])
            elif command == "/sendto":
                peer.send_to_contact(name=list[1], msg=list[2], type=list[3])
            elif command == "/contacts":
                peer.list_contacts()
            elif command == "/votefor":
                peer.vote_for(candidate=list[1])
            elif command == "/candidates":
                peer.list_candidates()
            elif command == "/exit":
                break