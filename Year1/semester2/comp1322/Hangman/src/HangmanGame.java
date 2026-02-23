
public abstract class HangmanGame {
    protected Word currentWord;
    protected GuessHandler guessHandler;
    protected  WordBank wordBank;
    protected GameUI ui;
    protected Difficulty difficulty;

    
    protected abstract WordBank getWordBank(String filePath);

    public HangmanGame(){
        initialise();
    }

    private void initialise(){
        wordBank = getWordBank("words.txt");
    }

    public boolean isInvalidDifficulty(){
        return wordBank.isBankEmpty();
    }


    public void startGame(){
        System.out.println("Welcome to Hangman! You have chosen " + getStringDifficulty() + " difficulty");
        String randomWord = wordBank.getRandomWord();
        this.currentWord = new Word(randomWord);
        this.guessHandler = new GuessHandler(currentWord, difficulty.getMaxAttempts());
        this.ui = new GameUI(currentWord, guessHandler);
        ui.DisplayWord();
        ui.DisplayGuessesLeft();
    }

    

    /**
     * Repeatidly asks for guess untill new guess is made
     * 
     *
     * @return The new guess
     */
    private char makeNewGuess(){
        while (true){
            char guess = CharacterInputHandler.readCharFromCmd("Enter a letter: ");
            if (guessHandler.checkGuessIsNew(guess)){
                return guess;
            } else{
                System.out.println("You have already guessed " + guess + ". Please guess a new letter.");
            }
        }
        
    }
    

    public void makeGuess(){
        System.out.println("");
        ui.DisplayGuessedLetters();

        
        char guess = makeNewGuess();
        guessHandler.logGuess(guess);

        if (guessHandler.wasGuessCorrect(guess)){
            ui.displayCorrectGuessMessage();
        } else{
            ui.displayIncorrectGuessMessage();
        }

        ui.DisplayWord();
        ui.DisplayGuessesLeft();

        checkGameStatus();

    }

    private void checkGameStatus(){
        if (currentWord.isGuessed()){
            ui.GameOverWinMessage();
        } else if (guessHandler.getGuessesRemaining() <= 0){
            ui.GameOverLossMessage();
        }
    }

    public boolean isGameOver(){
        return guessHandler.getGuessesRemaining() <= 0 || currentWord.isGuessed();
    }

    private String getStringDifficulty(){
        return difficulty.toString().toLowerCase();
    }
}
