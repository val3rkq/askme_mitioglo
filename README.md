# AskMe App

## Overview

Welcome to the **AskMe App** repository! This is a front-end web application built with **Tailwind CSS**. It allows users to ask questions, search for information, and interact with content.

#### Created for VK Education [2024, Autumn]

### Features:
- **Responsive Design**: The app is fully responsive using Tailwind CSS utility classes.
- **Interactive Forms**: Users can submit questions, search for content, and interact with the UI.
- **Scalable Architecture**: Easy to extend and maintain.

## Prerequisites

Before you get started, ensure you have the following installed on your machine:

- [Node.js](https://nodejs.org/en/) (version 14 or above)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Getting Started

Follow these steps to get a local copy of the project up and running:

### 1. Clone the repository

```bash
git clone https://github.com/val3rkq/askme-app.git
cd askme-app
```

### 2. Install dependencies
Run the following command to install all required npm packages (this will populate the node_modules/ folder):

```bash
npm install
```
### 3. Run Tailwind CSS build
You can compile the Tailwind CSS styles by running:

```bash
npm run build:css
```
This will compile the Tailwind CSS from src/tailwind_styles.css into the public/css/ directory.

### 4. Running the Project
For development purposes, you can run the app using Django’s development server (assuming it's part of a Django project), or serve the static files through any server of your choice.

If it’s part of a Django project, run the following command:

```bash
python manage.py runserver
```
Otherwise, use any static file server to preview your project locally.

## Customization
- **Modify CSS**: To change the styling, you can edit the src/tailwind_styles.css file and re-run the build process (npm run build:css).
- **Tailwind Configuration**: Adjust the Tailwind config by editing tailwind.config.js to include new colors, fonts, or spacing options.

## Contributing
If you'd like to contribute, feel free to submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.

- Fork the repository
- Create a new branch (git checkout -b feature-branch)
- Make your changes
- Push to the branch (git push origin feature-branch)
- Open a Pull Request

## License
This project is licensed under the MIT License. See the LICENSE file for details.

```css
This markdown provides a clean, simple `README.md` that outlines the basic steps for setting up
```