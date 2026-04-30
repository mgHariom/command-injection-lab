# step 1: Pick a base image (The OS/environment)
FROM python:3.9-slim

# step 2: Install system tools needed for the lab
RUN apt-get update && apt-get install -y iputils-ping

# step 3: Set the home dir inside the container
WORKDIR /app

# step 4: Copy local file to the container
COPY app.py .

# step 5: Install python dependencies
RUN pip install flask

# step 6: Expose the port that the app will run on
EXPOSE 5000

# step 7: Command to run the app
CMD ["python", "app.py"]