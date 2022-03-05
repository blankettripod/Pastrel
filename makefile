GCC = g++-11
GCCPARAMS = -Iinclude -Wall -Wextra -std=c++20 -Ofast -Wpedantic -Wno-unused-parameter -Werror
GCCDPARAMS = -Iinclude -Wall -Wextra -std=c++20 -Wpedantic -Wno-unused-parameter
LDFLAGS = -lm -Iinclude


HD  = $(wildcard include/**/*.h) $(wildcard include/*.h) $(wildcard include/**/**/*.h) $(wildcard include/**/**/**/*.h)
SRC = $(wildcard src/*.cpp)

OUTPUTDIR = bin/
OUTPUTFILE = Pastrel
LIBS =


$(OUTPUTDIR)$(OUTPUTFILE)Debug: $(SRC) $(HD)
	@mkdir -p $(OUTPUTDIR)
	$(GCC) -o $(OUTPUTDIR)$(OUTPUTFILE)Debug $(SRC) $(GCCDPARAMS) -g $(LDFLAGS) $(LIBS)

$(OUTPUTDIR)$(OUTPUTFILE): $(SRC) $(HD)
	@mkdir -p $(OUTPUTDIR)
	@echo $(HD)
	$(GCC) -o $(OUTPUTDIR)$(OUTPUTFILE) $(SRC) $(GCCPARAMS) $(LDFLAGS) $(LIBS)

run: $(OUTPUTDIR)$(OUTPUTFILE)
	@./$(OUTPUTDIR)$(OUTPUTFILE)

debug: $(OUTPUTDIR)$(OUTPUTFILE)Debug
	@gdb $(OUTPUTDIR)$(OUTPUTFILE)Debug



clean:
	@rm -rf $(OUTPUTDIR)*
	@clear