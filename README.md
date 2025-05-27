# CS50Quest

CS50Quest is a retro-inspired, turn-based RPG designed for programmers, especially those who have braved the legendary CS50 Introduction to Computer Science course. In this game, you explore a bug-infested dungeon, facing off against monsters based on real-world programming errors—think "Segmentation Fault," "Buffer Overflow," "Memory Leak," and the dreaded "Stack Overflow."  
Victory in battle requires not just brute force, but coding knowledge: monsters challenge you with programming quiz questions that can turn the tide of combat! The ultimate goal? Survive, learn, and reach the reward tile to unlock your CS50 diploma—proving your mastery over the course’s trickiest pitfalls.

---

## Project Overview

CS50Quest is both a game and an interactive educational tool. It combines classic pixel art, a battle system with a knowledge twist, and RPG exploration mechanics. Each enemy you face represents a common programming bug or error, with quiz questions crafted to help you internalize key CS50 concepts and real-world debugging wisdom.

The game is written entirely in Python using the Pygame library for graphics and user interaction. The modular codebase is organized for clarity and extensibility, allowing new monsters, questions, or features to be added easily.

---

## File Breakdown

- **main.py**  
  The entry point of the game. Handles initialization, the game loop, input events, collision detection, and manages the overall flow from the start of the dungeon to the reward screen.

- **config.py**  
  Stores game-wide constants: window size (`WIDTH`, `HEIGHT`), frames per second (`FPS`), window title, and background color. Centralizing these values makes adjustments and scaling straightforward.

- **map.py**  
  Contains the dungeon’s grid definition (`level_map`), tile size, and functions for drawing the map using Pygame surfaces. Each value in the map grid corresponds to a different tile type (grass, wall, or reward).

- **player/player.py**  
  Implements the `AnimatedPlayer` class, which controls the player’s position, movement (using arrow keys), sprite animation, and battle image. Designed for clean separation between player logic and the rest of the game.

- **monsters/enemy.py**  
  Defines the base `Enemy` class, including health, damage, speed, images, and pathfinding logic. This class is inherited by all specific monster types.

- **monsters/util.py**  
  Contains utility functions for monsters, including `astar` pathfinding (A* algorithm) and helper functions like finding the first walkable tile on the map.

- **monsters/segmentationFault.py**, **undefinedReference.py**, **memoryLeak.py**, **bufferOverFlow.py**, **stackOverFlowBoss.py**  
  Each of these files implements a unique enemy type inheriting from `Enemy`, setting custom HP, damage, images, and quiz questions/answers. Boss monsters (e.g., StackOverflowBoss) support multi-stage quizzes.

- **battle.py**  
  Handles the turn-based battle logic, drawing battle screens, animating sprites, and implementing the quiz mechanic. Correct answers heal the player, wrong answers can heal the enemy—mimicking how real bugs can “fight back.”

- **rewards/reward.py**  
  Implements the reward screen that appears upon reaching the victory tile, displaying a pixel-art CS50 certificate and a celebratory message.

- **assets/**  
  Directory containing all sprites, monster images, player animations, and reward images. These are referenced dynamically for extensibility and easy modding.

---

## Installation and Requirements

**Tested Python version:** `Python 3.10.9`

You must use **Python 3.10.9** (or another 3.x version, but the game was developed and tested specifically with 3.10.9) and the Pygame library.

> **IMPORTANT:** You must activate your Python virtual environment (`venv`) before installing dependencies or running the game. This ensures you have an isolated, compatible environment for CS50Quest.

```bash
# 1. Clone this repository
git clone https://github.com/ProjectXTN/CS50Quest
cd CS50Quest

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate your virtual environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies (always with venv activated)
pip install -r requirements.txt

If you forget to activate your virtual environment, the required packages might not be found when you try to run the game.
Always make sure your venv is activated before running or installing!

To run the game (with venv activated):

bash
Copier
Modifier
python main.py

How to Play

Arrow keys: Move your player character on the map.
SPACE: Attack during battles (when it’s your turn).
UP/DOWN arrows: Navigate quiz options.
ENTER: Confirm your quiz answer.

Any key or mouse click: Advance on victory/reward screens.

Explore the dungeon, approach monsters to trigger battles, and use both your combat skills and CS50 knowledge to win. When you defeat all monsters, head for the black "reward" tile to unlock your diploma!

Gameplay & Design Notes
Move with the arrow keys through a grid-based dungeon map, facing classic programming error monsters.

Each battle is turn-based. On enemy HP thresholds, a programming quiz is triggered—answer correctly to heal yourself; answer wrong and the enemy recovers HP.

Boss monsters feature multi-stage quizzes to test deeper knowledge.

The modular design (one file/class per component) was chosen to keep the project scalable and easy to extend, reflecting best Python practices and allowing easy addition of new monsters, tiles, or features.

All core logic is type-annotated for better readability, maintenance, and static analysis support.

All art and assets are stored in the assets/ folder, making it simple to swap sprites or expand the game visually.

Final Thoughts

CS50Quest is a tribute to everyone who’s wrestled with CS50's iconic bugs.
It aims to make learning (and reviewing) computer science fun, interactive, and a bit nostalgic.
Feel free to fork, contribute, or extend the project—there’s always another monster to defeat and another bug to squash!

Enjoy the adventure, and may your debugging always be victorious!

URL Video : https://www.youtube.com/watch?v=2rcp9eXLh1A&ab_channel=Youdidn%27texpectthis
Github : https://github.com/ProjectXTN/CS50Quest