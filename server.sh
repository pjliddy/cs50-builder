#!/bin/bash

# set up local machine to run Flask for Bootstrap Builder

# put Flask in debug mode and restart Flask when app code is changed

  export FLASK_DEBUG=1

# assign builder.py as the python app to run in Flask

  export FLASK_APP=builder.py

# launch Flask

  flask run
