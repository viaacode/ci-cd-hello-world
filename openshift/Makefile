VERSION = ${shell (git describe --tags || echo latest)}

.ONESHELL:
SHELL = /bin/bash

.PHONY: all

NAMESPACE = viaa-tools
OC_PROJECT = ${NAMESPACE}

APP_NAME = ci-cd-hello-world
IMAGE_NAME = ${NAMESPACE}/${APP_NAME}
REGISTRY = docker-registry-default.apps.do-prd-okp-m0.do.viaa.be
login:
	login_oc.sh https://do-prd-okp-m0.do.viaa.be:8443
	oc project "${OC_PROJECT}"
build:
	docker build -t "${REGISTRY}/${IMAGE_NAME}:${VERSION}" .
test:
	docker container run --name "${APP_NAME}_test" \
					--entrypoint python "${REGISTRY}/${IMAGE_NAME}:${VERSION}" \
					"-m" "pytest" "--cov=./app/" "--junit-xml=./tests/test_results.xml"
lint:
	docker container run --name "${APP_NAME}_lint" \
					--entrypoint flake8 "${REGISTRY}/${IMAGE_NAME}:${VERSION}" \
					--exit-zero \
					--max-line-length=88
push: 	login
	docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}

deploy-int:
	# There is no int component, so just tag
	oc tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:int
test-int:

deploy-qas:
	bash ./openshift/wait4rollout.sh qas ${APP_NAME} ${IMAGE_NAME} ${VERSION}
test-qas:


deploy-prd:
	bash ./openshift/wait4rollout.sh prd ${APP_NAME} ${IMAGE_NAME} ${VERSION}
approved:
	echo "Approved"

post-clean:
	docker container rm "${APP_NAME}_test"
	docker container rm "${APP_NAME}_lint"
