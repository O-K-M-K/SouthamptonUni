import java.util.HashMap;
import java.util.Map;

public class GuessHandler {
    private Map<Character, Letter> alphabet;
    private int guesses;
    private WordState currentWord;
    private boolean lastGuessCorrect;
    

    public GuessHandler(WordState currentWord, int guesses){
        this.currentWord = currentWord;
        this.guesses = guesses;

        this.alphabet = new HashMap<>();
        for (char c = 'a'; c <= 'z'; c++) {
            alphabet.put(c, new Letter(c));
        }
    }

    public void updateAlphabet(char letter){
        Letter l = alphabet.get(letter);
        l.guess();
    }

    public Letter getLetter(char letter){
        return alphabet.get(letter);
    }

    public boolean checkGuessIsNew(char guess){
        Letter l = alphabet.get(guess);
        return !l.isGuessed();
    }

    /**
     * Updates the alphabet of guessed letters. Updates the word if the guess was correct. If guess was incorrect decrements the remaining attempts.
     * @param guess
     *  
     */
    public void logGuess(char guess){
        updateAlphabet(guess);
        if (currentWord.containsGuess(guess)){
            currentWord.updateWord(guess);
            lastGuessCorrect = true;
        } else{
            decrementRemainingGuesses();
            lastGuessCorrect = false;
        }
    }

    public boolean wasGuessCorrect(char guess){
        return lastGuessCorrect;
    }

    public void decrementRemainingGuesses(){
        guesses -= 1;
    }
    public int getGuessesRemaining(){
        return guesses;
    }

}
