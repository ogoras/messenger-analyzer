# Messenger Analyzer

In order to use this tool, you need to [download your messages from Facebook](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/#:~:text=Open%20your%20Facebook%20account%20and,information%E2%80%A6%E2%80%9C%20(4).&text=On%20this%20page%20you%20can,want%20to%20download%20from%20Facebook.) in JSON format. Once it's downloaded, move the "messages" folder inside this repository.

To run, use:

```
python analyze.py [number of people to print] [number of words to print per person]
```

By default, the program prints 10 characteristic words for 10 people that have sent the most messages. The format is:
    
    ```
    [Name] [number of messages sent by the person]
    Vocabulary size: [number of distinct words the person used]
    1. [word] [the degree to which [word] is characteristic for the person] used [number of times the word was used by the person] times out of [number of times the word was used in total]
    2. ...
    ...
    10. ...

    ...
    ```
