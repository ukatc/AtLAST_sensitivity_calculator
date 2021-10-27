# This is a simple starter make file.
# See e.g. https://makefiletutorial.com/

# Define help as the default if make is called without a target
.DEFAULT_GOAL := help

#.PHONY: help test html clean

# It's good to have a 'make help' target to list the options, and a
# nice idea to have that run after a simple 'make', so the user doesn't
# need to know there is a 'help' target. 

# This is a regular comment, that will not be displayed.
# Help comments should be prefaced by double #
# Help comments are display with their leading whitespace. For
# example, all comments in this snippet are aligned with spaces.

## ----------------------------------------------------------------------
## This is a list of make targets.
## ----------------------------------------------------------------------

help:     ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

test:     ## Run pytest.
	PYTHONPATH=./src
	pytest

clean:    ## Delete temporary files.
