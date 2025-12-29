Description:
Webpage for analyzing natural language sentiment. Uses Naive Bayes and the Bag-of-words model (implemented with Python) to classify text sentiment as "Positive" or "Negative".

Example Output:
![](app.jpg)

Usage Instructions for Linux:

Step 1:
Install and start Docker if necessary. Open the terminal and enter `docker build -t myapp .` to build the Docker image. To run the application, enter `docker run -d -p 8080:8080 myapp`, or alternatively `docker run -d -p 8080:8080 -v $(pwd)/data:/app/data myapp` to save server-side user data for future logins.

Step 2:
Open a new tab in any browser and enter the url `http://localhost:8080/`.
