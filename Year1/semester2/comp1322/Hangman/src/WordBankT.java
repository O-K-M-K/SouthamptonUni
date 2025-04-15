import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class WordBankT {
    
    private List<String> easy_words = new ArrayList<>();
    private List<String> medium_words = new ArrayList<>();
    private List<String> hard_words = new ArrayList<>();

    private final Random rand = new Random();


    public WordBankT(String filePath){
        initialise(filePath);
    }

    private void initialise(String filePath){
        List<String> allWords = FileHandler.readWordsFromFile(filePath);
        categorizeWords(allWords);

    }

    private void categorizeWords(List<String> allWords){
        for (String line : allWords){
            String[] wordwithDifficulty = line.split(" ");

            //ensuring only correctly formatted words are
            if (wordwithDifficulty.length != 2){
                System.err.println("Invalid line format: " + line);
                continue;
            }

            switch (wordwithDifficulty[1]) {
                case "Easy" -> easy_words.add(wordwithDifficulty[0]);
                case "Medium" -> medium_words.add(wordwithDifficulty[0]);
                case "Hard" -> hard_words.add(wordwithDifficulty[0]);
                default -> System.err.println("Word with Unknown difficulty: " + wordwithDifficulty[1]);
            }
        }
    }

    public String getRandomWord(Difficulty difficulty){
        return switch (difficulty) {
            case EASY ->
                    easy_words.isEmpty() ? "No words available" : easy_words.get(rand.nextInt(easy_words.size()));
            case MEDIUM ->
                    medium_words.isEmpty() ? "No words available" : medium_words.get(rand.nextInt(medium_words.size()));
            case HARD ->
                    hard_words.isEmpty() ? "No words available" : hard_words.get(rand.nextInt(hard_words.size()));
            default -> "Invalid difficulty";
        };
    }
}
