import java.util.List;

public interface WordBank {

    List<String> getAllWords(String filePath);

    void categorizeWords(List<String> allWords);

    String getRandomWord();

    boolean isBankEmpty();
}
