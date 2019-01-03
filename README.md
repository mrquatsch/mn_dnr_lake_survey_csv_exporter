# MN DNR Lake Survey CSV exporter

Python app that runs inside of a docker container. The app scrapes the MN DNR site and grabs the latest survey information for every lake. The app produces a CSV file.

* There is an app directory that contains the python scripts. Inside of that is a properties file that contains the URLs used, the naming convention for the output file and the number of threads to use when pulling survies - the most time consuming part of the execution.

* The docker directory contains the docker file and the python requirements file. This is currently configured to use python 3.6

* Finally, there is a run.sh file; which is what should be executed. The run.sh builds the container, executes the container and mount your current directory in order to produce the output file

##### NOTE: Not all lakes have surveys
##### Funny note: The MN DNR doesn't even list 10,000 lakes

