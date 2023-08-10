# Swift_AI_bot

## Telegram Bot with YOLO5 Microservice and Jenkins Pipeline

Welcome to Swift_AI_bot, our feature-packed Telegram bot project! This bot is designed to handle various tasks, including image and video detection using the powerful YOLO5 microservice. Additionally, it boasts intelligent search capabilities with the /chagpt command and the ability to draw anything you desire through the /draw command. The project has been meticulously built and deployed using a Jenkins pipeline, simplifying the development and deployment processes.

## Features

- Image Detection: The bot can detect objects in images using the YOLO5 microservice.
- Video Detection: It can also perform object detection on videos using the same YOLO5 service.
- Intelligent Search: The /chagpt command allows users to search for specific content.
- Drawing Functionality: The /draw command enables users to request the bot to draw various objects or patterns.
- Jenkins Pipeline: The project follows a Jenkins pipeline to automate the build and deployment process.
- Kubernetes Deployment: The app is deployed on Kubernetes, ensuring scalability and availability.

## Project Structure

The repository contains code from our group project. It is a forked repository of the original repository, enriched with improvements and optimizations by our talented group members:


The repository is structured as follows:

- .idea: Contains IDE-specific configuration files (you can ignore this).
- Telegram_Bot: Holds the source code for the Telegram bot.
- Yolo5: Contains the YOLO5 microservice code for image and video detection.
- .gitignore: Specifies which files and folders should be ignored by Git.
- PullRequest.Jenkinsfile: Jenkinsfile for handling pull requests.
- bot-deployment.yaml: Kubernetes deployment file for the Telegram bot.
- build.Jenkinsfile: Jenkinsfile for the build stage of the pipeline.
- deploy.Jenkinsfile: Jenkinsfile for the deployment stage of the pipeline.
- yolo5-deployment.yaml: Kubernetes deployment file for the YOLO5 microservice.
- yolo5-service.yaml: Kubernetes service file for the YOLO5 microservice.



