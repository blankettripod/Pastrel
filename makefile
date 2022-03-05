GCC = g++-11
GCCPARAMS = -Iinclude -Wall -Wextra -std=c++20 -Ofast -Wpedantic -Wno-unused-parameter -Werror
GCCDPARAMS = -Iinclude -Wall -Wextra -std=c++20 -Wpedantic -Wno-unused-parameter
LDFLAGS = -lm -Iinclude


HD  = $(wildcard include/**/*.h) $(wildcard include/*.h) $(wildcard include/**/**/*.h) $(wildcard include/**/**/**/*.h)
SRC  = $(wildcard src/**/*.cpp) $(wildcard src/*.cpp) $(wildcard src/**/**/*.cpp) $(wildcard src/**/**/**/*.cpp)

OUTPUTDIR = bin/
OUTPUTFILE = Pastrel


$(OUTPUTDIR)$(OUTPUTFILE)Debug: $(SRC) $(HD)
	@mkdir -p $(OUTPUTDIR)
	$(GCC) -o $(OUTPUTDIR)$(OUTPUTFILE)Debug $(SRC) $(GCCDPARAMS) -g $(LDFLAGS) $(LIBS)

$(OUTPUTDIR)$(OUTPUTFILE): $(SRC) $(HD)
	@mkdir -p $(OUTPUTDIR)
	$(GCC) -o $(OUTPUTDIR)$(OUTPUTFILE) $(SRC) $(GCCPARAMS) $(LDFLAGS) $(LIBS)

run: $(OUTPUTDIR)$(OUTPUTFILE)
	@echo  
	@./$(OUTPUTDIR)$(OUTPUTFILE)

time: $(OUTPUTDIR)$(OUTPUTFILE)
	@echo 
	@time ./$(OUTPUTDIR)$(OUTPUTFILE)

debug: $(OUTPUTDIR)$(OUTPUTFILE)Debug
	@gdb $(OUTPUTDIR)$(OUTPUTFILE)Debug



clean:
	@rm -rf $(OUTPUTDIR)*
	@clear