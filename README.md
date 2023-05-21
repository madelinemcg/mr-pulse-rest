# Current Instructions to Run Locally

### Set Up

First, cd to the api folder, then run

`source mr-pulse-env/bin/activate`

to activate the python environment


Next, cd to the client folder and run

`yarn build`

this creates a production level build that flask will use (I may want to fix this in the future to not require building for testing purposes)


Assuming everything went fine, cd back to the api folder and run

`flask run`

to start up the server locally. It will have a link to the page and should work! Yay!


### Special Note
I have included some print statements in the front and back ends, the server prints will show up in the terminal, and frontend will show in the console (CTRL+SHIFT+I on the page).

This was mostly for debugging purposes but I thought you may find it helpful in order to understand how data is passed better.

