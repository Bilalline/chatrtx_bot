from http.client import HTTPConnection

def send_message(message):
    connection = HTTPConnection('192.168.1.57', 18137)
    headers = {'Content-type': 'text/plain; charset=utf-8'}
    # Кодируем сообщение в UTF-8
    encoded_message = message.encode('utf-8')
    connection.request('POST', '/', encoded_message, headers)
    response = connection.getresponse()

    if response.status == 200:
        return response.read().decode('utf-8')
    else:
        raise Exception("Error: Server responded with status {}".format(response.status))
