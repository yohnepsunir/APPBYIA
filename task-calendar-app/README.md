# Task Calendar App

## Overview
The Task Calendar App is a web-based application designed for task management and calendar functionalities. It allows users to create, read, update, and delete tasks, while also providing a user-friendly interface for managing their tasks effectively.

## Features
- Three-column interface: 
  - Task List
  - Task Editing Form
  - File Attachment Panel
- Each task includes:
  - Title
  - Description
  - Category
  - Priority (1-5)
  - Due Date
  - Status
- Full CRUD functionality for task management
- Local storage support for task persistence
- Docker containerization for easy local deployment

## Project Structure
```
task-calendar-app
├── backend
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── requirements.txt
│   └── .env
├── frontend
│   ├── index.html
│   ├── css
│   │   └── styles.css
│   ├── js
│   │   ├── app.js
│   │   ├── api.js
│   │   └── storage.js
│   └── assets
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yohnepsunir/APPBYIA.git
   cd task-calendar-app
   ```

2. Build and run the application using Docker Compose:
   ```
   docker-compose up --build
   ```

3. Access the application in your web browser at `http://localhost:5000`.

### Usage
- Use the interface to add new tasks, edit existing ones, and manage your task list.
- Tasks will be stored in local storage for persistence across sessions.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.