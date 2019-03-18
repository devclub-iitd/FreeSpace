# Free-Space

## Introduction
This app allows the students of IIT Delhi to know which Lecture Halls are free at a particular time of the day.

## Installing the app
First, clone the repository.use <pre> git clone</pre>
Go to the repository's folder and then create a virtual environment.

Create a virtual environment and activate it.<br>
Install the requirements.

### Using virtualenv 

 <pre> $ python3 -m virtualenv FreeSpace
 $ . FreeSpace/bin/activate
 $ pip install -r requirements.txt </pre>
 
### Using Anaconda
 <pre>$ conda create -n FreeSpace --yes python=3.*
$ conda activate FreeSpace
$ pip install -r requirements.txt</pre>
 
 You are good to go.
## Running the app
 For generating the tables which get shown on the site, run
 <pre>$ ./folderCreate.sh
$ python3 html_generator.py</pre>
 
 Then view the site by running
 <pre>$ python3 -m http.server 8080
$ sensible-browser http://localhost:8080</pre>
 
