# Social Dev Forum

## What is this ?

The goal is to create a social forum where amateur and professional devs can collaborrate on a social platform.

## Backend

This application is currently split into the following backend services:

* A [users](users/) service for management of user authentication/validation.
* A [forum](forum/) service for management of the forum posts themselves. 

### Users Backend

The users service is an HTTP REST service written in [Python](https://python.org) with the [FastAPI](https://fastapi.tiangolo.com/) framework.

A MySQL server is used for longterm data storage and a Redis service is used for ephemeral session storage.

More details can be found in [users/README](users/README.md)

### Forum Backend

The forum service is an HTTP REST service written in C# using the .NET framework.

More details can be found in [forum/README](forum/README.md)