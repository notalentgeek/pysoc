## To do list.
* Demonize the Flask server for debugging purpose. I need a Nodemon - like utility but for Flask, [https://nodemon.io/](https://nodemon.io/).
    * [http://flask.pocoo.org/docs/0.12/deploying/](http://flask.pocoo.org/docs/0.12/deploying/), official guide of deployment option from the Flask official website.
    * [http://gunicorn.org/](http://gunicorn.org/), Gunicorn website.
    * [http://stackoverflow.com/questions/6337119/how-do-you-daemonize-a-flask-application](http://stackoverflow.com/questions/6337119/how-do-you-daemonize-a-flask-application), some say that the solution might be using Gunicorn.
* Make more database class to be more agnostic. At this moment `database.py` is strictly made for RethinkDB. Although RethinkDB is open source, the main company behind it just went close (on October 2016, I think), so I am not sure if there will be update. But, all in all there are still people using RethinkDB.
    1. Possible alternative I can think of.
        * MongoDB seems like the go - to choice for NoSQL database.
        * SQLite, I like SQLite portability. However, I am not sure if this is ambitious.
    1. Priority when choosing database server.
        1. Easy to learn. This is relative, but some says PostgreSQL is the hardest to learn. 
        1. Intended to be for real - time system.
        1. Nice server interface included. For example, default server interface for RethinkDB is set at port 8080.
        1. OpenSource!
        1. Platform agnostic, I saw there are some database build for specific platform (Amazon AWS, Microsoft Azure , ...). I prefer not to use these.
        1. Popular among developer (StackOverflow discussion, ...). Check here as well, [http://db-engines.com/en/ranking](http://db-engines.com/en/ranking), a website like DistroWatch but for database.
        1. Portable as SQLite.
        1. Preferably NoSQL type database (CouchDB, MongoDB). This because I never use relational database like SQL, I could/want to learn though. [http://db-engines.com/en/ranking/document+store](http://db-engines.com/en/ranking/document+store), check here!
* Make sure server have a recovery system. When it returns an error or exception, resets it automatically.
    * [https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04), a lot of people is talking about UWSGI, I think that might be the solution. However, this guide is intended for Ubuntu 14.04, while the server that is currently running is using Ubuntu LTS 16.04.
    * [https://www.digitalocean.com/community/tutorials/how-to-set-up-highly-available-web-servers-with-keepalived-and-floating-ips-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-highly-available-web-servers-with-keepalived-and-floating-ips-on-ubuntu-14-04), how to setup high availability server using floating IP in Ubuntu 14.04.
* Make sure server running when the system starts and __NOT__ when SSH logged in.
