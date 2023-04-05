## Telegram bot - Ask Me About Programming Bot

This Telegram bot is designed to simplify the learning of programming languages, new technologies, or any other theoretical knowledge that needs to be reviewed from time to time.

The Telegram bot can send you quiz questions that you must answer correctly. It will also provide information with an explanation of the answer.

![Peek 2023-03-31 03-14](https://user-images.githubusercontent.com/84034483/228993102-3f2cb30e-c56a-4c94-bcf8-c247a35a6aca.gif)


In case you do not want to choose an answer from multiple options, you can select a simple question that you can answer on your own and compare the answer with the correct option.

![Peek 2023-03-31 03-21](https://user-images.githubusercontent.com/84034483/228993182-64e12f8a-9c8f-4db5-a36c-3fc1e76c67ff.gif)

For convenient addition and editing of questions, the application has a web interface written in Flask, which is a kind of admin panel.

Through it, you can add a new topic for questions, add and edit questions, delete questions, and also view questions in the form of a table that can be sorted to find the needed question.

## Launch of the project

* ![Python Version](https://img.shields.io/badge/python-3.11-green) ![Code Style](https://img.shields.io/badge/code%20style-black-blue)
* PostgreSQL 15.1 database
* Install dependencies from requirements.txt: `pip install -r requirements.txt`
* To connect to the database, add to the environment variables in the .env.example file, **rename the file to .env**:
  - `DB_NAME` (name of your PostgreSQL database)
  - `DB_USER` (your PostgreSQL username)
  - `DB_PASSWORD` (password of your PostgreSQL user)
  - `DB_HOST` (your PostgreSQL database host)
  - `DB_PORT` (port of your PostgreSQL database)
* If you are running the project for the first time, you need to create tables in the database. To do this, you need to run the models.py file from the questions module.
* After the tables have been created, run the admin panel through the wsgi.py file in the project root.
* Finally, add your question threads and questions via the admin panel.
* Run the bot through the bot_app.py file in the ask_me_bot package.

## Running the admin panel on the local network
* For Unix systems - install gunicorn

`pip install gunicorn`
* To run the application, enter the command

`gunicorn --bind 127.0.0.1:5000 wsgi:app`

* Alternative option for Windows systems - install waitress

`pip install waitress` 

* To run the application, enter the command

`waitress-serve --listen=127.0.0.1:5000 wsgi:app`

<details>
  <summary>
    <b>Setting up request proxying with nginx:</b>
  </summary>

  * Install nginx on your system. For ubuntu, use the command `sudo apt install nginx`
    
  <details>
    <summary>
      If you do not have Ubuntu, but Manjaro, like me. And when installing nginx, there are no required folders.
    </summary>

   * Insall nginx:
    
   `sudo pacman -S nginx`

   * Create directories:
  
   `sudo mkdir /etc/nginx/sites-enabled`

   `sudo mkdir /etc/nginx/sites-available`

   `sudo mkdir /etc/nginx/conf.d`
   * Edit the config, connect the sites-enabled folder:
    
   `sudo nano /etc/nginx/nginx.conf`
    

   ```
    http {
        
        ##
        # Paste these lines into the http block in your config
        ##
    
        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
        
    }
   ```
  
  </details>
 
   * Create a config file for the application 
    
   `sudo nano /etc/nginx/sites-available/ask_me_bot.conf`

   ```
    server {
        listen 80;  
        
        access_log /var/log/nginx/ask_me_bot.access.log;
        error_log /var/log/nginx/ask_me_bot.error.log; 
        
        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }    
   ```

   * Add a link to config to the sites-enabled folder
    
   `sudo ln -s /etc/nginx/sites-available/ask_me_bot.conf /etc/nginx/sites-enabled/`
   * Restart the server

   `sudo systemctl restart nginx`
   
  #### We can check the admin panel at 127.0.0.1 (By default, nginx runs on port 80, you can change it in the config to any free port.) 
</details>



