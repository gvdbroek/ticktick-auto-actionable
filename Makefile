IMAGE_NAME := gvdbroek/ticktick-actionable

build:
	BUILDKIT=1 docker build --tag ${IMAGE_NAME} .
rebuild:
	BUILDKIT=1 docker build --tag ${IMAGE_NAME} --no-cache .
run:
	docker run --rm --env-file .env ${IMAGE_NAME}
run-it:
	docker run --rm --env-file .env -it ${IMAGE_NAME} sh
clean:
	docker image prune -a
