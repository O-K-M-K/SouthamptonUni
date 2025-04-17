import java.util.List;
import java.util.Random;

public class RandomWordStrategy implements WordSelectionStrategy {
    private final Random rand = new Random();

    @Override
    public String selectWord(List<String> wordList){
        return wordList.get(rand.nextInt(wordList.size()));
    }
}
