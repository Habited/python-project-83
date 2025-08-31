install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer.app:app run

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .


PORT ?= 10000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

build: install
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app