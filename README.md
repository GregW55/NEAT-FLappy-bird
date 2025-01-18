# Flappy Bird AI with NEAT

This project uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train an AI to play a Flappy Bird clone. The game features dynamically moving pipes, animated birds, and a scoring system, with NEAT optimizing bird behavior over multiple generations.

---

## Features
- **AI-Driven Gameplay**: Trains birds to play the game using the NEAT algorithm.
- **Customizable NEAT Configuration**: Modify the `config-feedforward.txt` file to experiment with different neural network structures and parameters.
- **Smooth Graphics**: Built using Pygame for seamless animations and gameplay.
- **Dynamic Scoring System**: Tracks the score and generations during gameplay.

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Pygame: `pip install pygame`
- NEAT-Python: `pip install neat-python`

### Installation
1. Clone the repository:
   git clone https://github.com/GregW55/flappy-bird-ai.git
   cd flappy-bird-ai
Install the required Python libraries:

pip install -r requirements.txt
Ensure the imgs/ directory contains the necessary assets:

bird1.png, bird2.png, bird3.png: Bird animation sprites
pipe.png: Pipe image
base.png: Ground image
bg.png: Background image
Update the NEAT configuration:

The config-feedforward.txt file contains all parameters for the NEAT algorithm. Customize these values to tweak the AI behavior.
Usage
Run the script:

python main.py
Watch as the birds evolve to play the game more effectively over generations.

To stop the simulation, close the game window.

# How It Works
Bird Movement: Birds are controlled by a neural network that takes the bird's position and pipe distances as inputs and decides whether to jump.
Pipe Collision: Pipes move toward the bird, and collisions are detected using masks.
Base Movement: The base scrolls to simulate movement.
Fitness Function: Birds are rewarded for surviving and passing pipes but penalized for collisions or falling.

# Configuration
The config-feedforward.txt file allows you to modify the neural network and NEAT parameters:

pop_size: Adjust the number of birds in each generation.
activation_default: Define the activation function for neurons.
max_fitness_threshold: Set a fitness value to terminate training early.

# Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

# License
This project is licensed under the MIT License.
