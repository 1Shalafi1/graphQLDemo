build:
	docker build -t graphql .

run:
	docker run -d --name graphql_demo -p 80:80 graphql	

compose:
	docker-compose -f docker-compose.local.yml up -d --build

db-init:
	docker exec -i database pg_restore -U postgres -d graphql < ./fixtures/db_dump/dvdrental.tar

db-psql:
	docker exec -it database psql -U postgres -d graphql