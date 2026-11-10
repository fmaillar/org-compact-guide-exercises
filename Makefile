.PHONY: check emacs-check
check:
	python3 scripts/verify.py

emacs-check:
	emacs -Q --batch -l setup/init.el -l scripts/check_org.el
