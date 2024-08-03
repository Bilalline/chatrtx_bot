import random
import string
import json
import requests

def join_queue(session_hash, fn_index, ip,  port, chatdata):
    python_object = {
        "data": chatdata,
        "event_data": None,
        "fn_index": fn_index,
        "session_hash": session_hash
    }
    json_string = json.dumps(python_object)

    url = f"http://{ip}:{port}/queue/join"
    response = requests.post(url, data=json_string)

def listen_for_updates(session_hash, ip, port):
    url = f"http://{ip}:{port}/queue/data?session_hash={session_hash}"

    response = requests.get(url, stream=True)
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line[5:])
                if data['msg'] == 'process_completed':
                    return data['output']['data'][0][0][1]
            except Exception as e:
                pass
    return ""

def send_message(message, ip, port):
    if not port:
        find_chat_with_rtx_port()
    if not port:
        raise Exception("Failed to find a server port for 'Chat with RTX'. Ensure the server is running.")

    session_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    #add chat history here -v
    chatdata = [[[message, None]], None]
    join_queue(session_hash, 34, ip, port, chatdata)
    return listen_for_updates(session_hash, ip, port)