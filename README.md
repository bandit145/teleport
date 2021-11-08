# teleport
Teleport interview project

### Testing this program
Configure a Python virtualenv: (This program was developed on python3.8, any versions newer then that should work fine) 
```virtualenv venv```

Start venv: ```source venv/bin/activate```

Install dependencies: ```pip install -r dev-requirements.txt -r requirements.txt```

Run tests: ```make test``` or ```python -m pytest tests/```

### Building your own container
Run ```make build``` or ```docker build -t bandit145/conn-track:latest .```.

### Running the program
On any host with docker run the following command to pull and run the programs container image.

Metrics will be available on port 9000; there is one counter called new_connections.

(If you built a container in the last section on the host you execute this on this will run that one, if you want to pull the one from docker hub remove the image you created from your local image store.)

```docker run --cap-add=NET_ADMIN --network host bandit145/conn-track:latest```