python3 -m venv .venv

source .venv/bin/activate

# ensure you have (.venv) in your terminal
# ensure in vscode showing ~('venv': '.venv')
# edit port number in rtx_api_3_5.py if you restarted chatrtx ui

pip install -r requirements.txt
echo "TOKEN=AAA:BBBB" > .env

python3 rtx.py


docker build -t bilalline/chatrtx_bot:3 .
docker push bilalline/chatrtx_bot:3


docker run -e TOKEN= \
           -e IP=192.168.1.57 \
           -e PORT=18137 \
           -e GROUP_CHAT_LOG=-1002165280593 \
           bot:2