I used the anonypy library to help implement all the privacy algorithms. 
However, after pip installing and following the provided example I ran into a bug. I ended up needing to go into the soruce code files and making a fix there.
As a result, when packaging the application into a Docker container I can not simply install the library through pip anymore and must use this locally modified version.

This folder is storing that entire anonypy library for which I made a modification.