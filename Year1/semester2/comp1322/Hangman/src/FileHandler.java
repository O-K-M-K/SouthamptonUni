import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;


public final class FileHandler {
    /**
     * 
     * @param filePath
     * @return Array where each element is a new line in the text file
     */
    public static List<String> readWordsFromFile(String filePath){
        if (filePath == null || filePath.trim().isEmpty()){
            throw new IllegalArgumentException("File path cannot be null or empty");
        }
        List<String> allWords = new ArrayList<>();
        List<String> words = List.of("chimpanzee Medium", "practice Medium", "resolution Medium", "export Medium", "call Easy",
"colour Medium", "qualification Hard", "transport Hard", "cower Hard", "scenario Hard",
"intervention Hard", "hour Easy", "to Easy", "we Easy", "extreme Hard", "need Easy",
"reader Hard", "apparatus Hard", "reproduction Hard", "guerrilla Hard", "carrot Medium",
"mars Easy", "pitch Easy", "wild Easy", "rifle Easy", "lie Easy", "paragraph Medium",
"lighter Medium", "herd Medium", "deter Medium");
        List<String> backupWords = new ArrayList<>(words);

        Path path = Paths.get(filePath);

        try(BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)){
            String line;
            while ((line = reader.readLine()) != null){
                allWords.add(line.trim());
            }
            reader.close();
        } catch (IOException e){
            System.err.println("Error reading file: " + e.getMessage() + "\n Reverting to deafult wordlist");
            return backupWords;
            //throw new RuntimeException("Failed to read file");
        }
        return allWords;
    }

    

}
