Input user's prompt:  "Write tetris game in python use pygame.

Final prompt (combined instruction and best answer) : 

Do not simplify anything it is waste of time.
Compare with original functionality.
Do not explain, just generate full code in one shot.
Use exactly how and what is in that instructions and requirements to implement it in best way, fully working solution.
"""To develop a Tetris game in Python using the Pygame library, follow these steps:

1. **Set Up the Environment**:
   - Install Pygame: Ensure Pygame is installed in your Python environment (pip install pygame).
   - Import necessary libraries: Import Pygame and other required modules.

2. **Initialize Pygame**:
   - Initialize Pygame and set up the game window with an appropriate size for a Tetris game grid.

3. **Define Game Constants and Variables**:
   - Define constants such as screen dimensions, grid size, colors, and shapes of Tetris pieces.
   - Create a list of the seven Tetris shapes (I, O, T, S, Z, J, L) and their rotations.

4. **Create Game Functions**:
   - **Draw Grid**: Function to draw the game grid and update it as pieces move.
   - **Generate New Piece**: Function to generate a new Tetris piece at the top of the grid.
   - **Move Piece**: Functions to handle moving the piece left, right, down, and rotating it.
   - **Check Collision**: Function to check for collisions with the grid boundaries or other pieces.
   - **Clear Lines**: Function to check for and clear completed lines, updating the score.
   - **Game Over**: Function to check if new pieces can no longer be placed, indicating game over.

5. **Game Loop**:
   - Create a main game loop to handle user input, update game state, and render the screen.
   - Handle user inputs for moving and rotating pieces.
   - Update the game state by moving pieces down at regular intervals.
   - Check for collisions and clear lines as needed.
   - Render the updated game grid and pieces on the screen.

6. **Display and Scoring**:
   - Update the display to show the current score, level, and next piece.
   - Implement a scoring system that awards points for clearing lines and increases the level as more lines are cleared.

7. **End Game and Restart**:
   - Implement functionality to detect game over and allow the player to restart the game.

By following these steps, you can create a functional Tetris game using Python and Pygame. Each step involves breaking down the task into manageable functions and ensuring the game logic is correctly implemented to provide a smooth and enjoyable gameplay experience."""
