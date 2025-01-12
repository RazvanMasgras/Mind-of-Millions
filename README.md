# Mind of Millions
### Authors - 324CD
#### Masgras Răzvan-Andrei - Backend Logic (Open Trivia DB)
#### Șerban Dumitru-Alexandru - Frontend Logic (Pygame)
### Link: https://github.com/RazvanMasgras/Mind-of-Millions.git

## Overview

Mind of Millions is a game inspired by the well-known show, "Who Wants to Be a Millionaire?". It is built using Python libraries such as `pygame`, `requests`, and `html`.

The core functionality of the game mirrors the show: players are presented with a series of general knowledge questions and four answer choices. The goal is to win the prize of 1 million dollars, with the help of up to three lifelines.

## Features

- **Interactive Gameplay**: Engaging and interactive quiz game with sound effects and animations.
- **Lifelines**: Includes lifelines like Fifty-Fifty, Phone a Friend, and Audience Poll to assist players.
- **Dynamic Question Generation**: Fetches and prepares trivia questions from the Open Trivia Database.
- **Responsive Design**: Adjusts text size and wraps text to fit within the designated areas on the screen.

## Technologies Used

- **Python**: The primary programming language used for the development of the game.
- **Pygame**: A set of Python modules designed for writing video games. It provides functionalities like creating windows, drawing shapes, handling events, and playing sounds.
- **Requests**: A simple HTTP library for Python, used to fetch trivia questions from the Open Trivia Database.
- **HTML**: Used for parsing and handling HTML content within the game.
- **Open Trivia Database**: An online database of trivia questions used to dynamically generate questions for the game.
- **Git**: Version control system used for tracking changes in the source code and collaborating with team members.
- **GitHub**: Hosting service for the Git repository, used for project management and collaboration.

## Masgras Răzvan-Andrei

### Contributions

#### Backend & Unit Testing

- **Backend Logic**: Developed the core backend logic to fetch and parse trivia questions from the Open Trivia Database using the `requests` library. Implemented error handling to manage API request failures and ensure a smooth user experience.
- **Unit Tests**: Created comprehensive unit tests in the `test_backend.py` file to validate the functionality of the backend logic. These tests cover various scenarios, including successful data retrieval, handling of API errors, and data parsing accuracy.

#### Sound and Music Effects

- **Sound Effects**: Integrated sound effects for various game actions, such as button clicks and correct/incorrect answers, to enhance the interactive experience. Utilized the `pygame` library to load and play sound files.
- **Music**: Added background music for the main menu and ending screen to create an immersive atmosphere. Ensured smooth transitions between different music tracks based on game events.

#### Text Wrapping for Questions

- **Dynamic Text Wrapping**: Implemented a text wrapping mechanism to ensure that trivia questions fit within the designated areas on the screen. This feature adjusts the text size and wraps long questions to multiple lines, maintaining readability and a clean user interface.

### Challenges

The backend of the game was easier to implement, therefore the most difficult part was communicating with my colleague with how to integrate our solutions.

I had some bugs when implementing lifelines, and it was indeed helpful to write unit tests, because they helped me identify where the errors were.

There were problems with text wrapping and I solved them by defining a method which centers the text and wraps it.

## Șerban Alexandru-Dumitru

### Contributions

- **GUI Development**: Designed and implemented the graphical user interface (GUI) using the `pygame` library. Created various menus and screens, including the main menu, game screen, and ending screen, ensuring a cohesive and visually appealing user experience.
- **Menu and Screen Navigation**: Developed a system for navigating between different menus and screens. Implemented button actions and transitions to provide a smooth and intuitive user interface.
- **Image Handling**: Searched for and edited images to be used as backgrounds, buttons, and other visual elements within the game. Ensured that all images were appropriately sized and formatted for use in `pygame`.
- **Button Actions and Animations**: Implemented interactive buttons with animations and sound effects. Added visual feedback for button presses to enhance the interactive experience.
- **Score and Prize System**: Developed a scoring system to track the player's progress and calculate the prize amount based on the number of correct answers. Displayed the current score and potential prize on the game screen to keep players informed of their progress.

### Challenges

- Adding animation for answer selection
    - **Solution**: made the function to alternate between different images that reflect the state of the button

- Matching text with buttons
    - **Solution**: created a button class with fields to help

## Design

The main menu of Mind of Millions offers two exciting game modes:

- **Normal Mode**: This mode consists of 15 questions that progressively increase in difficulty. Players must answer each question correctly to advance to the next level, with the ultimate goal of winning 1 million dollars.
- **Endless Mode**: In this mode, players can select the categories they are interested in and answer an unlimited number of questions. This mode is perfect for those who want to test their knowledge across various topics without the pressure of a final prize.

Both modes provide an engaging and challenging experience, catering to different player preferences.

The game also benefits of interactive buttons that display animations when pressed, sound effects for buttons and music in the main menu and on the ending screen.

## Installation

To install the project, clone the repository and install the dependencies:

```bash
git clone https://github.com/RazvanMasgras/Mind-of-Millions.git
cd Mind-of-Millions
pip install -r requirements.txt
```

## Usage

To start the project, run the following command:

```bash
python3 main.py
```
