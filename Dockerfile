FROM python:3.10.12
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

ENV TOKEN=
ENV IP=
ENV PORT=
ENV GROUP_CHAT_LOG=

CMD ["python3", "/app/rtx.py"]

