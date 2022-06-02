# Messenger Analyzer

## Prerequisites
In order to use this tool, you need to [download your messages from Facebook](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/#:~:text=Open%20your%20Facebook%20account%20and,information%E2%80%A6%E2%80%9C%20(4).&text=On%20this%20page%20you%20can,want%20to%20download%20from%20Facebook.) in JSON format. The first time you run one of the scripts, please specify the path to the downloaded folder. Afterwards, the script will remember your last used path.

## Scripts
Currently, there are 2 scripts that you can use:
- `analyze_vocabulary`: Analyze vocabulary in your messages.
- `find_words`: Find specific words in your messages.

## Usage

To run, use from the root directory:
```
python -m src.script_name [arguments]
```

For example, to analyze vocabulary for the first time, use:
```
python -m src.analyze_vocabulary --input "C:/Users/John/Documents/facebook-johndoe4"
```

For help, use the -h flag. For instance:
```
python -m src.find_words -h
```

## Unit testing
Before running this command, make sure you're in the root directory. To run unit tests, use:
```
python -m unittest
```