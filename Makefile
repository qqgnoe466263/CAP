CC = gcc
CFLAGS = -O1 -g -Wall -Werror -I.

GIT_HOOKS := .git/hooks/applied
all: $(GIT_HOOKS) test

# Control the build verbosity
ifeq ("$(VERBOSE)","1")
    Q :=
    VECHO = @true
else
    Q := @
    VECHO = @printf
endif

# Enable sanitizer(s) or not
ifeq ("$(SANITIZER)","1")
    # https://github.com/google/sanitizers/wiki/AddressSanitizerFlags
    CFLAGS += -fsanitize=address -fno-omit-frame-pointer -fno-common
    LDFLAGS += -fsanitize=address
endif

$(GIT_HOOKS):
	@scripts/install-git-hooks
	@echo

OBJS := http_parser.o http_server.o main.o
deps := $(OBJS:%.o=.%.o.d)

http_server: $(OBJS)
	$(VECHO) "  LD\t$@\n"
	$(Q)$(CC) $(LDFLAGS) -o $@ $^ 

%.o: %.c
	$(VECHO) "  CC\t$@\n"
	$(Q)$(CC) -o $@ $(CFLAGS) -c -MMD -MF .$@.d $<

test: http_server scripts/driver.py
	$(VECHO) " TEST\t$<\n"
	$(Q) ./http_server > /dev/null & scripts/driver.py -c
	$(Q) kill `pidof http_server`

run: http_server
	./http_server 

valgrind_existence:
	@which valgrind 2>&1 > /dev/null || (echo "FATAL: valgrind not found"; exit 1)

valgrind: valgrind_existence
	# Explicitly disable sanitizer(s)
	$(MAKE) clean SANITIZER=0 http_test
	$(eval patched_file := $(shell mktemp /tmp/http_test.XXXXXX))
	cp http_test $(patched_file)
	chmod u+x $(patched_file)
	sed -i "s/alarm/isnan/g" $(patched_file)
	scripts/driver.py -p $(patched_file) --valgrind
	@echo
	@echo "Test with specific case by running command:" 
	@echo "scripts/driver.py -p $(patched_file) --valgrind -t <tid>"

clean:
	rm -f $(OBJS) $(deps) *~ http_test /tmp/http_test.*
	(cd traces; rm -f *~)

-include $(deps)
