# UDCLogsAnalysis

This is the Logs Analysis project, the third from Udacity's full stack web developer program.
The program will answer three query questions with three seperate SQL queries, and present the output
in the console.  Additionally, there is a .txt file to verify what the output should be.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
pick the platform package for your respective operating system.

You will then need to install [Vagrant](https://www.vagrantup.com/downloads.html)
which is software that configures a virtual Machine

You will then need to download the VM configuration.
Additionally, you will need to download the data and configure your directory.  All of this information can be found  [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

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
