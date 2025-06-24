# Usage:
#   1. Build the image: 
#       docker build --tag PetrPlihal/trafi .
#   2. Run the container: 
#       docker run --detach --publish 5000:5000 --name trafi-dev PetrPlihal/trafi


# 1. Start from an official Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependencies file and install them
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 4. Copy the rest of the application code into the container
COPY app/ .

# 5. Tell Docker the container listens on port 5000 (Flask's default)
EXPOSE 5000

# 6. Define the command to run your app when the container starts
CMD ["flask", "run", "--debug"]