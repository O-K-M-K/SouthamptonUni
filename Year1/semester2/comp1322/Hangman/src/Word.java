import java.util.ArrayList;
import java.util.List;

public class Word {

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

    public String getWord(){
        return word;
    }

    public List<Letter> getLetters(){
        return letters;
    }

    public boolean isGuessed(){
        for (Letter l : letters){
            if (!l.isGuessed()){
                return false;
            }
        }
        return true;
    }




}
