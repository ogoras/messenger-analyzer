# Messenger Analyzer

In order to use this tool, you need to [download your messages from Facebook](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/#:~:text=Open%20your%20Facebook%20account%20and,information%E2%80%A6%E2%80%9C%20(4).&text=On%20this%20page%20you%20can,want%20to%20download%20from%20Facebook.) in JSON format. Once it's downloaded, move the "messages" folder inside this repository.

For now you have to edit the source for it to work. In `analyze.py`, line 24 please change:
```py
for sender in ["your name", "your friend's name"]:
```
swapping your name to your Facebook name and your friend's name to your friend's Facebook name.

To run, use:

```
python analyze.py
```
