# Binghamton University, Spring 2023

## CS428/528 Project-2: Proxy Server

### SUMMARY

Part 1:
Multi-threaded web server implementation to support a multi-threaded web proxy server. Assume that caching is not enabled on the proxy server. In this case, the
main functionality of the proxy server is to forward requests received from the client to the web server and forward responses received from the web server to the client

Part 2:
In part 2, A typical proxy server will cache the web pages each time the client makes a particular request for the first time. The basic functionality of caching works as follows. When the proxy gets a request, it checks if the requested object is cached and if yes, it returns the object from the cache without contacting the server. If the object is not cached, the proxy retrieves it from the server, returns it to the client, and caches a copy for future requests. The proxy also verifies that the cached responses are still valid.


### NOTES, KNOWN BUGS, AND/OR INCOMPLETE PARTS

N/A

### REFERENCES

[List any outside resources used]: #

### INSTRUCTIONS

Part 1:

When the proxy server forwards a request to the web server or forwards a response to the client, it should print the following information on the terminal:
proxy-forward,DESTINATION,THREAD-ID,TIMESTAMP
Where “DESTINATION” is either client or server.
Also, modify your web server implementation to print the following information on the terminal
whenever it responds to a request:
server-response,STATUS-CODE,THREAD-ID,TIMESTAMP
Where the "STATUS-CODE" is the HTTP response code indicating the result of the request.

Part 2:

When there is a cache hit in the proxy, and it is valid, the proxy should print the following
information on the terminal after sending the cached response to the client:
proxy-cache,client,THREAD-ID,TIMESTAMP

### SUBMISSION

I have done this assignment completely on my own. I have not copied it, nor have I given my solution to anyone else. I understand that if I am involved in plagiarism or cheating I will have to sign an official form that I have cheated and that this form will be stored in my official university record. I also understand that I will receive a grade of "0" for the involved assignment and my grade will be reduced by one level (e.g., from "A" to "A-" or from "B+" to "B") for my first offense, and that I will receive a grade of "F" for the course for any additional offense of any kind.

By signing my name below and submitting the project, I confirm the above statement is true and that I have followed the course guidelines and policies.

Submission date: 26-03-2023

Team member 1 name: Shreevara Andila

Team member 2 name: Saran Pal Thanikonda

