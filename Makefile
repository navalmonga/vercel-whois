HOST=127.0.0.1
TEST_PATH=./

start:
	python vercel_whois.py
clean-cd:
	rm chromedriver*
clean-pyc:
	rm -f *.pyc
	rm -f *.pyo
	rm -rf __pycache__
	echo 'clean-pyc completed.'

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

install-cd:
	curl https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip -o chromedirver_mac64.zip
	unzip chromedirver_mac64.zip
	rm chromedirver_mac64.zip
install:
	pyenv install 2.7.16
	python --version
pip-install:
	pip install -r requirements.txt
isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

docker-run:
	docker build \
		--file=./Dockerfile \
		--tag=my_project ./
	docker run \
		--detach=false \
		--name=my_project \
		--publish=$(HOST):8080 \
		my_project