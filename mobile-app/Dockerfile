# Frontend Dockerfile for React Native Web Build
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies for Expo
RUN npm install -g expo-cli serve

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose port for Expo dev server and web
EXPOSE 19000 19001 19002 8081

# Start Expo development server (use Expo Go app on mobile to access)
CMD ["npx", "expo", "start", "--host", "lan"]
