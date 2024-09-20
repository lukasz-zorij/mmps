Input prompt : Write tetris game in python use pygame.

Do not simplify anything it is waste of time.
Compare with original functionality.
Do not explain, just generate full code in one shot.
Use exactly how and what is in that instructions and requirements to implement it in best way, fully working solution.
"""To develop a Tetris game in Python using the Pygame library, you need to follow these key steps:
1. **Setup Environment**:
   - Install Python and Pygame.
   - Create a project directory and set up your working environment.
2. **Initialize Pygame**:
   - Import the Pygame library and initialize it.
   - Set up the game window with a defined width and height.
3. **Define Game Constants**:
   - Define constants for screen dimensions, block size, grid dimensions, colors, and game speed.
4. **Create Game Grid**:
   - Develop a function to create and manage the game grid.
   - Represent the grid as a 2D list to track filled and empty cells.
5. **Define Tetromino Shapes**:
   - Define the shapes of different Tetrominoes (I, O, T, S, Z, J, L) using multi-dimensional arrays.
   - Store these shapes in a list or dictionary for easy access.
6. **Handle Tetromino Movement**:
   - Implement functions to move Tetrominoes left, right, down, and rotate them.
   - Ensure movements respect grid boundaries and do not overlap with filled cells.
7. **Collision Detection**:
   - Create a function to check for collisions with the grid boundaries and other Tetrominoes.
   - Ensure Tetrominoes stop moving when they collide and lock into place.
8. **Line Clearing**:
   - Develop logic to check for and clear complete lines in the grid.
   - Shift remaining lines down and update the score accordingly.
9. **Game Loop**:
   - Implement the main game loop to handle events, update game state, and render graphics.
   - Include event handling for user inputs (e.g., arrow keys for movement, space bar for rotation).
10. **Game Over Condition**:
    - Check for game over conditions (e.g., blocks reaching the top of the grid).
    - Display a game over message and provide options to restart or quit.
11. **Rendering**:
    - Create functions to draw the grid, Tetrominoes, and other game elements (e.g., score, next piece preview).
    - Use Pygame's drawing functions to render shapes and text.
12. **Main Function**:
    - Combine all the components in a main function to initialize the game and start the game loop.
By following these steps, you can structure and implement a Tetris game in Python using Pygame."""