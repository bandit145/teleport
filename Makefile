test:
	python -m pytest tests/
build:
	docker build -t bandit145/conn-track:latest .