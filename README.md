python3 -m venv .venv

source .venv/bin/activate

# ensure you have (.venv) in your terminal
# ensure in vscode showing ~('venv': '.venv')
# edit port number in rtx_api_3_5.py if you restarted chatrtx ui

pip install -r requirements.txt
echo "TOKEN=AAA:BBBB" > .env

python3 rtx.py
