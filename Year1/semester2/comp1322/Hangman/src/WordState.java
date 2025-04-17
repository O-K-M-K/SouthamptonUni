import java.util.List;

public interface WordState {

    boolean containsGuess(char letter);
    void updateWord(char guess);
    String getWord();
    List<Letter> getLetters();
    boolean isGuessed();
}
