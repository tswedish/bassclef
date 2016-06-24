
# Copyright 2015, 2016 Thomas J. Duck <tomduck@tomduck.ca>

# This file is part of bassclef.
#
#  Bassclef is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License verson 3 as
#  published by the Free Software Foundation.
#
#  Bassclef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with bassclef.  If not, see <http://www.gnu.org/licenses/>.


# Preamble -------------------------------------------------------------------

# Exits if errors occur in a pipe chain
SHELL = /bin/bash -o pipefail

# Clean up on error (https://www.gnu.org/software/make/manual/make.html#Errors)
.DELETE_ON_ERROR:

# Executables
PYTHON3 = python3
PANDOC = pandoc
CONVERT = convert

# Variables to store targets from each module
ALL =
CLEAN =


# Functions -------------------------------------------------------------------

# $(call config,name): gets value from config.ini
config = $(PYTHON3) -c "from scripts import util;\
                        print(util.config('$(1)'))"

# $(call getmeta,filename,varname): gets metadata value for doc
getmeta = $(PYTHON3) -c "from scripts import util;\
                         print(util.getmeta('$<', '$(1)'))"

# $(call copyfiles,src,dest): copies files from source to destination
define copyfiles
@if [ ! -d $(dir $(2)) ]; then mkdir -p $(dir $(2)); fi;
@if [ -f $(1) ]; then echo "cp $(1) $(2)"; fi;
@if [ -f $(1) ]; then cp $(1) $(2); fi;
endef


# Paths -----------------------------------------------------------------------

WEBROOT = $(shell $(call config,webroot))

TMP := $(shell mktemp -d /tmp/bassclef.XXXXXXXXXX)
ifeq ($(TMP),)
$(error Temporary directory could not be created.)
endif


# Module imports --------------------------------------------------------------

MODULES = $(wildcard */module.mk)
include $(MODULES)


# Default rule----------------------------------------------------------------

.DEFAULT_GOAL =

all: $(ALL)


# Deploy rules ---------------------------------------------------------------

serve:
	mkdir -p www
	cd www && $(PYTHON3) -m http.server


# Housekeeping rules ---------------------------------------------------------

clean:
	@echo "Removing files and directories from www/..."
	@rm -rf $(CLEAN)
	@find www -type d -empty -delete

.PHONY: $(ALL) serve clean