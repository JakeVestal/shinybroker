import asyncio
import socket
import struct
import select

from shinybroker.functionary import functionary
from shinybroker.utils import pack_message


def create_ibkr_socket_conn(host='127.0.0.1', port=7497, client_id=0):
    # Returns a socket connection, the API_VERSION, and the CONNECTION_TIME,
    #   in a tuple

    # create the socket object
    ib_socket = socket.socket()
    try:
        ib_socket.connect((host, port))
    except ConnectionRefusedError as noconn:
        print(noconn)
        print(
            "Couldn't connect to an IBKR client at host: " + host + \
            "; port: " + str(port) + ".\n" + \
            "Make sure that there is a running instance of TWS or IBG at " + \
            "that host & port,\n" + \
            "and that the API settings in the client have been configured " + \
            "to accept a connection!"
        )

    ib_socket.send(
        str.encode("API\0", 'ascii') +
        pack_message(
            "v%s..%s" % (
                functionary['minimum_client_version'],
                functionary['maximum_client_version']
            )
        ) +
        pack_message(
            functionary['outgoing_msg_codes']['START_API'] + "\0" +
            "2" + "\0" +  # VERSION
            str(client_id) + "\0\0"
        )
    )


    # If connection is successful, then the api will respond with a message
    #   that contains the API version you're connected under and the
    #   starting date-timestamp of the connection, so read this once.
    (rd, wt, er) = select.select([ib_socket], [], [])
    handshake_msg_size = struct.unpack("!I", rd[0].recv(4))[0]
    handshake_msg = list(
        filter(
            None,
            [x.decode('ascii') for x in ib_socket.recv(
                handshake_msg_size
            ).split(b"\x00")]
        )
    )

    API_VERSION = handshake_msg[0]
    CONNECTION_TIME = handshake_msg[1]

    return ib_socket, API_VERSION, CONNECTION_TIME


# make an async function that can be awaited so that we know if there's a
# message available to be read.
async def socket_has_data(s):
    return select.select([s], [], [])


async def ib_msg_reader(sock, sesh, verb):
    while True:
        (rd, wt, er) = await socket_has_data(sock)
        msg_prefix = rd[0].recv(4)
        msg_size = struct.unpack("!I", msg_prefix)[0]
        msg = list(
            filter(
                None,
                [x.decode('ascii') for x in sock.recv(
                    msg_size
                ).split(b"\x00")]
            )
        )
        if verb:
            print(msg)
        try:
            sesh.send_custom_message(msg[0], msg[1:])
        except AttributeError:
            pass


def ib_msg_reader_run_loop(ib_sock, shiny_sesh=None, verbose=False):
    asyncio.run(ib_msg_reader(sock=ib_sock, sesh=shiny_sesh, verb=verbose))


def ib_msg_reader_sync(sock):
    (rd, wt, er) = select.select([sock], [], [])
    msg_prefix = rd[0].recv(4)
    msg_size = struct.unpack("!I", msg_prefix)[0]
    msg = list(
        filter(
            None,
            [x.decode('ascii') for x in sock.recv(
                msg_size
            ).split(b"\x00")]
        )
    )
    return msg

