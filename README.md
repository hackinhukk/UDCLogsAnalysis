# UDCLogsAnalysis

This is the Logs Analysis project, the third from Udacity's full stack web developer program.
The program will answer three query questions with three seperate SQL queries, and present the output
in the console.  Additionally, there is a .txt file to verify what the output should be.

This project sets up a mock PostGreSQL database for a fictional news website.  The main.py script uses the psycopg2 library to query the database and create a report that answers three questions from the fictional data in the database:

1) What are the most popular three articles of all time?

2) Who are the most popular article authors of all time?

3) On which days did more than 1% of requests lead to errors?

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
pick the platform package for your respective operating system.

You will then need to install [Vagrant](https://www.vagrantup.com/downloads.html)
which is software that configures a virtual Machine

In the project repository, you will see a file named Vagrantfile.  Please do not alter it, as the file correctly configures the virtual machine as is.
Additionally, you will need to download the news data database.  You can do so  [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

```
Give examples
```

### Installing

After your Vagrant machine finishes downloading from calling Vagrant up in the vagrant directory you installed,
you should type
```
vagrant ssh
```
and press enter in the Vagrant bash terminal.  After you get into the virtual environment, type
  ```
  cd /vagrant
  ```
and enter.  Once you're in this directory, type
```
cd UDCLogsAnalysis
```
and press enter.  Then type
```
python main.py
```
and press enter.  The answer should appear on your bash terminal output.  An example file of what the output should
look like is found in the output.txt file.

NOTE: There are no views that you need to setup before running the queries.


### And coding style tests

The python code follows PEP8 Standards.



## Built With

* [Vagrant](https://www.vagrantup.com/) - Virtual Machine to run the PostGreSQL Server
* [PostgreSQL](https://www.postgresql.org/) - Open Source Relational Database
* [Python](https://www.python.org/) - Programming Language (Version 2.7)

## Contributing

There are no plans to accept contributions at this time.

## Authors

* **Trevor Thomas**


## License

This project is not under any license.
