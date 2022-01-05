import threading
from multiprocessing import process

from push.push_manager import PushManager


def serve_forever(port, auth_key):
    m = PushManager(address=('', port), authkey=auth_key)
    mgmt_server = m.get_server()
    mgmt_server.stop_event = threading.Event()
    process.current_process()._manager_server = mgmt_server
    try:
        accepter = threading.Thread(target=mgmt_server.accepter, daemon=True)
        accepter.start()
        return m, accepter
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
