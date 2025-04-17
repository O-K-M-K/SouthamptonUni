import java.util.ArrayList;
import java.util.List;

public class Word implements WordState {

    private final String word;
    private List<Letter> letters;
    

    public Word(String word) {
        if (word == null || word.isEmpty()){
            throw new IllegalArgumentException("Word cannot be null or empty");
        }
        this.word = word;
        this.letters = new ArrayList<>();
        initialiseLetters();
    }

    private void initialiseLetters(){
        for (char c : word.toCharArray()){
            letters.add(new Letter(c));
        }
    }

    @Override
    public String getWord(){
        return word;
    }

    @Override
    public List<Letter> getLetters(){
        return letters;
    }

    @Override
    public boolean isGuessed(){
        for (Letter l : letters){
            if (!l.isGuessed()){
                return false;
            }
        }
        return true;
    }

    @Override
    public boolean containsGuess(char letter){
        for (Letter l : letters){
            if (l.getValue() == letter && !l.isGuessed()){
                return true;
            }
        }
        return false;
    }

    @Override
    public void updateWord(char guess){
        for (Letter l : letters){
            if (l.getValue() == guess){
                l.guess();
            }
        }
    }


}
