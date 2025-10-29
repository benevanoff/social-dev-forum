# Social Dev Forum

## What is this ?

The goal is to create a social forum where amateur and professional devs can collaborrate on a social platform.

## Forum Service

The forum service should be able to accept new posts and store them persistently so that they can be viewed by website visitors or other forum members.

### Installation

#### Dependencies

* git (https://github.com/git-guides/install-git)
* C# ASP.NET 9 (https://dotnet.microsoft.com/en-us/download/dotnet/9.0)

#### Instructions

First, clone this repository `git clone https://github.com/benevanoff/social-dev-forum.git`.

Navigate to the root directory of this git project, `social-dev-forum/`.

To run the application, use `dotnet run`.

### Technical Design

#### Forum Post Creation

A user should be able to create a new post with the following features:

* A post subject
* A text body for the post

To accomplish this, we will need to be able to accept form submissions over the web (REST API on the backend with a frontend form). The frontend will connect to the backed by making an API call to the backend, containing the form page input data.

Backend API:

```
REQUEST

POST /create

HEADER {"Content-Type": "application/json"}

BODY
{
  "subject" : "I made this app!",
  "body": "It is a calculator"
}

RESPONSE

{
  "post_id": 1
}

```

#### Forum Post Fetching/Reading/Rendering

All users should be able to view any other post which has been previously submitted to the server.

```
REQUEST

GET /post/?id=1

RESPONSE

{
  "subject" : "I made this app!",
  "body": "It is a calculator"
}
```

#### List All Forum Posts

Return a list of all post IDs available along with their post subjects.

```
REQUEST

GET /list

RESPONSE
[
 {
   "id": 1,
   "subject": "I made this app!"
 },
 {
  "id": 2,
  "subject": "This is an example"
 }
]
```
