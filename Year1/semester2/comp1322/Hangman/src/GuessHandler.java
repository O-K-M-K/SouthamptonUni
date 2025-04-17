import java.util.HashMap;
import java.util.Map;

public class GuessHandler {
    private Map<Character, Letter> alphabet;
    private int guesses;
    private WordState currentWord;
    

    public GuessHandler(WordState currentWord, int guesses){
        this.currentWord = currentWord;
        this.guesses = guesses;

        this.alphabet = new HashMap<>();
        for (char c = 'a'; c <= 'z'; c++) {
            alphabet.put(c, new Letter(c));
        }
    }

    public void guessLetter(char letter){
        Letter l = alphabet.get(letter);
        l.guess();
    }

    public Letter getLetter(char letter){
        return alphabet.get(letter);
    }

    public Map<Character, Letter> getAlphabet(){
        return alphabet;
    }

    public boolean checkGuessIsNew(char guess){
        Letter l = alphabet.get(guess);
        return !l.isGuessed();
    }

    /**
     * Updates the alphabet of guessed letters. Updates the word if the guess was correct. If guess was incorrect decrements the remaining attempts.
     * @param guess
     * @return true if guess was correct false if not 
     */
    public boolean logGuess(char guess){
        guessLetter(guess);
        if (currentWord.containsGuess(guess)){
            currentWord.updateWord(guess);
            return true;
        } else{
            decrementGuess();
            return false;
        }
    }


    public void decrementGuess(){
        guesses -= 1;
    }
    public int getGuessesRemaining(){
        return guesses;
    }

}
