import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Hangman {

    public static void main(String[] args) {
        GameUI.welcomeMessage();
        

        HangmanGame game = selectGameDifficulty();
      
        if (game != null){
            game.startGame();
            while (!game.isGameOver()){
                game.makeGuess();
            }
            GameUI.thanksForPlayingMessage();
        } else{
            System.err.println("Error game object is null.");
        }

        
    }

    /**
     * Allows the user to select a game difficulty and returns the appropriate HangmanGame instance.
     * Handles cases where words for a specific difficulty might not be available.
     *
     * @return A configured HangmanGame instance of the selected difficulty
     */
    //alter so word bank is inserted into hangman game meaning you create it here and they have seperate lifetimes
    private static HangmanGame selectGameDifficulty() {
        List<Character> availableDifficulties = new ArrayList<>(Arrays.asList('e', 'm', 'h'));

        while (!availableDifficulties.isEmpty()) {
            GameUI.displayDifficulties(availableDifficulties);
            
            char choice = CharacterInputHandler.readValidatedCharFromCmd(
                    "Enter your choice (e/m/h): ",
                    availableDifficulties);

            HangmanGame game = createGameInstance(choice);

            // Check if the selected difficulty has available words
            if (game.isInvalidDifficulty()) {
                handleInvalidDifficulty(availableDifficulties, choice);
            } else {
                return game;
            }
        }

        return null;
    }

    /**
     * Creates a HangmanGame instance based on the difficulty choice.
     *
     * @param choice The difficulty character ('e', 'm', or 'h')
     * @return A new HangmanGame instance of the appropriate difficulty
     */
    private static HangmanGame createGameInstance(char choice) {
        return switch (choice) {
            case 'e' -> new EasyHangmanGame();
            case 'm' -> new MediumHangmanGame();
            case 'h' -> new HardHangmanGame();
            default -> throw new IllegalArgumentException("Invalid difficulty choice: " + choice);
        };
    }

    /**
     * Handles the case where a selected difficulty has no available words.
     * Removes the invalid difficulty from available options and asks the user
     * if they want to try another difficulty.
     *
     * @param availableDifficulties List of currently available difficulties
     * @param invalidChoice The difficulty that was found to be invalid
     */
    private static void handleInvalidDifficulty(List<Character> availableDifficulties, char invalidChoice) {
        System.out.println("No words available for that difficulty.");

        // Remove the invalid difficulty from available options
        availableDifficulties.remove(Character.valueOf(invalidChoice));

        // Check if there are any difficulties left
        if (availableDifficulties.isEmpty()) {
            System.out.println("There are no valid difficulties in the word bank. " +
                    "Please check the text file and ensure the only difficulties are 'Easy', 'Medium', or 'Hard'.");
            System.exit(1);
        }

        // Ask if the user wants to try another difficulty
        Character continueChoice = CharacterInputHandler.readValidatedCharFromCmd(
                "Would you like to choose another difficulty (y/n): ",
                Arrays.asList('y', 'n'));

        if (continueChoice != 'y') {
            System.out.println("Exiting game due to lack of words.");
            System.exit(0);
        }
    }

}
