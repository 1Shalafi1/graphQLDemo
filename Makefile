build:
	docker build -t graphql .

run:
	docker run -d --name graphql_demo -p 80:80 graphql	

compose:
	docker-compose -f docker-compose.local.yml up -d --build
