# EnzyHTP-GPT
A web application that serves as an interface between a user and EnzyHTP's workflows.

# Developers: First Time Install
* First, clone this repository onto your local machine.
* We will then need to create a conda environment to run the website.
  * Create a new conda environment and install Flask using the command `conda install -c anaconda flask`.
  * This is the only package we have to install as of now, but when we integrate EnzyHTP, we will need to install many more.
* To run the website, open two terminals on VSCode.
  * On one, cd into the `flask-server` folder and run `python server.py` to start the backend.
  * On the other, run `npm i` and `npm start` in the `client` folder.
* That's it! The website should begin running on `localhost:3000`.
