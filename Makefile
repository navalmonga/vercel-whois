HOST=127.0.0.1
TEST_PATH=./

clean-pyc:
	rm -f *.pyc
	rm -f *.pyo
	rm -rf __pycache__
	echo 'clean-pyc completed.'

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

install:
	pyenv install 2.7.16
	pyenv local 2.7.16
	python --version
	pip install -r requirements.txt

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	python pywhois.py

docker-run:
	docker build \
		--file=./Dockerfile \
		--tag=my_project ./
	docker run \
		--detach=false \
		--name=my_project \
		--publish=$(HOST):8080 \
		my_project