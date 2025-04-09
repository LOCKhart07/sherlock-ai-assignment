# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m sherlock

# Set the working directory to /code and change ownership
WORKDIR /code
RUN chown -R sherlock:sherlock /code

# Switch to the non-root user
USER sherlock

# Copy and install dependencies
COPY --chown=sherlock:sherlock ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --user --no-warn-script-location

# Copy application code
COPY --chown=sherlock:sherlock ./ /code

# Ensure user-installed packages are in PATH
ENV PATH="/home/sherlock/.local/bin:${PATH}"

# Expose the port
EXPOSE 3000

# Set the maintainer
LABEL maintainer="Jenslee Dsouza <dsouzajenslee@gmail.com>"

# Start Uvicorn with the root path
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000", "--proxy-headers"]