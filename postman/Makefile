STUDIO_USERNAME ?= easy
STUDIO_PASSWORD ?= dev

TENANT ?= $(STUDIO_USERNAME)-configeditor
SCHEME ?= https:
DOMAIN ?= sandbox.socotra.com

STUDIO_URL ?= $(SCHEME)//studio.$(DOMAIN)

# studio = tenant MGMT UI; the stock "test user" is "alice.lee" (optional)

TENANT_USERNAME ?= easy.dev
TENANT_PASSWORD ?= easy-dev
TENANT_HOSTNAME ?= $(TENANT).co.$(DOMAIN)

API_ENV   ?= sandbox
API_TOKEN ?= jwt
API_URL   ?= $(SCHEME)//api.$(DOMAIN)

JSON_BASIS       ?= easy_dev
JSON_COLLECTION  ?= $(shell pwd)/$(JSON_BASIS).postman_collection.json
JSON_ENVIRONMENT ?= $(shell pwd)/$(JSON_BASIS).postman_environment.json

# run the Postman collection and environment as configured above
test:
	@# TODO: export environment variables before newman run, or use
	@[ -x "$(shell command -v newman)" ] \
		|| ( echo 1>&2 '--- install newman' ; exit 1 )
	@echo '--- tenant: $(TENANT_HOSTNAME)'
	newman run "$(JSON_COLLECTION)" \
		--environment "$(JSON_ENVIRONMENT)" $(ARGS)
.PHONY: test
