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
The app requires the user to manually login to the roombooking <a href="">site</a>. Once logged in, get the cookie with name <b>PHPSESSID</b> and pass it as an argument to the python script along with how the number of weeks you want to scrape the data for. not specifying the argument, takes the default value of <b>2</b>.

For generating the tables which get shown on the site, run
<pre>$ python tableGen.py [COOKIE_ID] [WEEKS_TO_SCRAPE]</pre>
 
 Then view the site by running
 <pre>$ python3 -m http.server 8080& sensible-browser http://localhost:8080</pre>
 
## NOTE
The room booking site only shows the tables from the day after, so for debugging purposes, it is recommended to move forward your system's date by 1.
