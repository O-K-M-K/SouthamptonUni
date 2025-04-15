
public abstract class HangmanGame {
    protected Word currentWord;
    protected GuessHandler guessHandler;
    protected  WordBank wordBank;
    protected GameUI ui;
    protected Difficulty difficulty;

    protected abstract int getMaxAttempts();
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
        String randomWord = getWord();
        this.currentWord = new Word(randomWord);
        this.guessHandler = new GuessHandler(currentWord, getMaxAttempts());
        this.ui = new GameUI(currentWord, guessHandler);
        ui.DisplayWord();
    }

    private String getWord(){
        return wordBank.getRandomWord();
    }

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

        //log guess
        if (guessHandler.logGuess(guess)){
            System.out.println("Correct!");
        } else{
            System.out.println("Incorrect!");
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
