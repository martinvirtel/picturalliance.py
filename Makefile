SHELL := /bin/bash


README.md : README.md.sh
	{ \
	TMPFILE=/tmp/$$$$.tmp ;\
	trap "rm -f $$TMPFILE" EXIT ;\
	./$< >$$TMPFILE && mv $$TMPFILE $@ ;\
	}


