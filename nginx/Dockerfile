# Use an official NGINX runtime as a parent image
FROM nginx:latest

# Copy your NGINX configuration file to the container
COPY /nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 22
EXPOSE 22

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
