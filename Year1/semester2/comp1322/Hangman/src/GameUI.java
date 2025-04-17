public class GameUI {

    private final Word word;
    private final GuessHandler guessHandler;

    public GameUI(Word word, GuessHandler guessHandler){
        this.word = word;
        this.guessHandler = guessHandler;
    }

    public void DisplayWord(){
        System.out.print("Your word: ");
        for (Letter l : word.getLetters()){
            if (l.isGuessed()){
                System.out.print(l.getValue() + " ");
            } else {
                System.out.print("_ ");
            }
        }
        System.out.println("");
    }

    public void DisplayGuessedLetters(){
        System.out.print("Letters left to guess: ");
        for (char c = 'a'; c <= 'z'; c++) {
            Letter letter = guessHandler.getLetter(c);
            if (letter != null) {
                if (letter.isGuessed()) {
                    System.out.print("#" + " ");
                } else {
                    System.out.print(letter.getValue() + " ");
                }
            }
        }
        System.out.println(); // Newline for clarity
    }

    public void GameOverLossMessage(){
        System.out.println();
        System.out.println("Game over! You've run out of attempts.");
        System.out.println("The word was: " + word.getWord());

    }

    public void GameOverWinMessage(){
        System.out.println();
        System.out.println("Congratulations you win!");
        System.out.println("You had " + guessHandler.getGuessesRemaining() + " guesses left.");
    }

    public void DisplayGuessesLeft(){
        System.out.println("Guesses left: " + guessHandler.getGuessesRemaining());
    }
}
