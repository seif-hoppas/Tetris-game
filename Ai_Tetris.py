import time, pygame
import tetris_base as base

# Set up the display
size   = [640, 640]
screen = pygame.display.set_mode((size[0], size[1]))

# Function to calculate level and fall frequency based on score
def calculate_level_and_fall_freq(score):
    """
    Calculate the level and fall frequency based on the score.

    Args:
        score (int): The current score.

    Returns:
        tuple: A tuple containing the level and fall frequency.
    """
    level     = int(score / 400) + 1
    fall_freq = 0.0000002 - (level * 0.02)
    return level, fall_freq

# Function to run the game with a given chromosome
def run_game(chromosome, speed, max_moves = 500, show = False):
    """
    Run the Tetris game with a given chromosome.

    Args:
        chromosome (Chromosome): The chromosome representing the Tetris strategy.
        speed (int): The speed of the game.
        max_moves (int, optional): The maximum number of moves before ending the game. Defaults to 500.
        show (bool, optional): Whether to display the game graphics. Defaults to False.

    Returns:
        int: The final score of the game.
    """
    base.FPS = int(speed)
    base.main()

    # Initialize game variables
    board            = base.get_blank_board()
    last_fall_time   = time.time()
    score            = 0
    level, fall_freq = calculate_level_and_fall_freq(score)
    falling_piece    = base.get_new_piece()
    next_piece       = base.get_new_piece()

    # Calculate best move for the falling piece using the chromosome
    chromosome.calculate_best_move(board, falling_piece)

    num_moves = 0

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Game exited by user")
                exit()

        # If falling piece is None, get a new piece and calculate the best move
        if falling_piece is None:
            falling_piece = next_piece
            max_moves -= 1
            next_piece    = base.get_new_piece()

            chromosome.calculate_best_move(board, falling_piece,show)

            num_moves += 1
            score += 1

            last_fall_time = time.time()

            # Check if the game is over
            if (not base.is_valid_position(board, falling_piece)):
                break

        # Update falling piece position and score
        if time.time() - last_fall_time > fall_freq:
            if (not base.is_valid_position(board, falling_piece, adj_Y=1)):
                base.add_to_board(board, falling_piece)

                num_removed_lines = base.remove_complete_lines(board)
                if(num_removed_lines == 1):
                    score += 40
                elif (num_removed_lines == 2):
                    score += 120
                elif (num_removed_lines == 3):
                    score += 300
                elif (num_removed_lines == 4):
                    score += 1200

                level, fall_freq = calculate_level_and_fall_freq(score)
                falling_piece = None
            else:
                falling_piece['y'] += 1
                last_fall_time = time.time()

        # Render the game if 'show' is True
        if show:
            base.DISPLAYSURF.fill(base.BGCOLOR)
            base.draw_board(board)
            base.draw_status(score, level, max_moves)
            base.draw_next_piece(next_piece)

            if falling_piece is not None:
                base.draw_piece(falling_piece)

            pygame.display.update()
            base.FPSCLOCK.tick(base.FPS)

        # Check if the game is over based on the maximum number of moves
        if max_moves <= 0 or score > 2400000:
            print("YOU BROKE THE RECORD WOW!")
            break

    return score
