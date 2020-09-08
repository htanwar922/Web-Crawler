#!/bin/bash

if [[ -z "$VIRTUAL_ENV" ]]; then
	python3 -m pip install virtualenv
	virtualenv `dirname $BASH_SOURCE`/venv
	source `dirname $BASH_SOURCE`/venv/bin/activate
else
	source "$VIRTUAL_ENV"/bin/activate		# not required
fi


printf "\n\n\nDEACTIVATE VIRTUAL_ENV AFTER USE ...\nRun deactivate \n\n\n"

pip3 install -r `dirname $BASH_SOURCE`/requirements.txt

python3 `dirname $BASH_SOURCE`/main.py --root_url https://flinkhub.com

#rm -rf "$VIRTUAL_ENV"
#deactivate
