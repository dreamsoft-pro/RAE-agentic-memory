up:
	docker compose -f infra/docker-compose.yml up -d --build

down:
	docker compose -f infra/docker-compose.yml down

migrate:
	@echo "Apply DDL on Postgres on container start via initdb.d"

seed:
	python -c "print('seed placeholder')"

eval:
	python eval/run_eval.py
