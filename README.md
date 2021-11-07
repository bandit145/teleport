# teleport
Teleport interview project

### Testing this program
Configure a Python virtualenv: (This program was developed on python3.8, any versions newer then that should work fine) 
```virtualenv venv```

Start venv: ```source venv/bin/activate```

Install dependencies: ```pip install -r dev-requirements.txt -r requirements.txt```

Run tests: ```make test``` or ```python -m pytest tests/```



### Running the program
On any host with docker run the following command to pull and run the programs container image.

```docker run --cap-add=NET_ADMIN --network host bandit145/conn-track:latest```