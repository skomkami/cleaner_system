To run program you have to have PyGraphviz installed system wide. For ubuntu use command:
```bash
sudo apt-get install graphviz graphviz-dev
```

In order to install all dependencies required run command posted down below in terminal.

```bash
pip install -r requirements.txt
```

### Custom building map file

To choose custom map config file add the path to it as a script argument.

e.g: `python main.py maps/c2.json`

File `maps/floor0.json` is default one – when no arguments provided.