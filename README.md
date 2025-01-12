# Mind of Millions

## Overview

Mind of Millions is a game inspired by the well-known show, "Who Wants to Be a Millionaire?". It is built using Python libraries such as `pygame`, `requests`, and `html`.

The core functionality of the game mirrors the show: players are presented with a series of general knowledge questions and four answer choices. The goal is to win the prize of 1 million dollars, with the help of up to three lifelines.

## Features

- **Interactive Gameplay**: Engaging and interactive quiz game with sound effects and animations.
- **Lifelines**: Includes lifelines like Fifty-Fifty, Phone a Friend, and Audience Poll to assist players.
- **Dynamic Question Generation**: Fetches and prepares trivia questions from the Open Trivia Database.
- **Responsive Design**: Adjusts text size and wraps text to fit within the designated areas on the screen.

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
