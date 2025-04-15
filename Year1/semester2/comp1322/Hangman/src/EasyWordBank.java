import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class EasyWordBank implements WordBank {

    private List<String> words = new ArrayList<>();
    private final Random rand = new Random();

    public EasyWordBank(String filePath){
        categorizeWords(getAllWords(filePath));
    }

    @Override
    public List<String> getAllWords(String filePath){
            List<String> allWords = FileHandler.readWordsFromFile(filePath);
            return allWords;
    }

    @Override
    public void categorizeWords(List<String> allWords){
        for (String line : allWords){
            String[] wordwithDifficulty = line.split(" ");

            //ensuring only correctly formatted words are
            if (wordwithDifficulty.length != 2){
                System.err.println("Invalid line format: " + line);
                continue;
            }
            if (wordwithDifficulty[1].equals("Easy")){
                words.add(wordwithDifficulty[0]);
            }
            
        }
    }


    @Override
    public String getRandomWord(){
        String randomWord = "";
        if (words.isEmpty()){
            System.err.println("No easy words available");
        } else{
            randomWord = words.get(rand.nextInt(words.size()));
        }
        return randomWord;
    }

    @Override
    public boolean isBankEmpty(){
        return words.isEmpty();
    }

}
