import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;


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

        Path path = Paths.get(filePath);

        try(BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)){
            String line;
            while ((line = reader.readLine()) != null){
                allWords.add(line.trim());
            }
            reader.close();
        } catch (IOException e){
            System.err.println("Error reading file: " + e.getMessage());
            System.exit(0);
            //throw new RuntimeException("Failed to read file");
        }
        return allWords;
    }

    

}
