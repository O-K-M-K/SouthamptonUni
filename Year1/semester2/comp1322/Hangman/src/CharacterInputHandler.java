import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

public final class CharacterInputHandler {

    private static final BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

    public static Character readValidatedCharFromCmd(String message, List<Character> validChars){
        boolean valid = false;
        Character input = null;

        while (!valid){
            input = readCharFromCmd(message);
            valid = validChars.contains(input);
            if (!valid){
                System.out.print("Invalid input. Please only input: ");
                for (Character ch : validChars){
                    System.out.print(ch + " ");
                }
                System.out.println();
            }

        }

        return input;
    }


    /**
     * 
     * Reads a command line input and will only accept it if it is a single alphabetical character.
     * @param input
     * @return the inputted character
     */
    public static Character readCharFromCmd(String message){

        boolean valid = false;
        String input = "";

        while (!valid){
            System.out.print(message);
            input = readStringInternal();
            if (validateInput(input)){
                valid = true;
            } else {
                System.out.println("Invalid input");
            }
        }
        return input.trim().charAt(0);
    }

    /**
     * String is only valid if it is a single alphabetical character. Any whitespace will be trimmed
     * @param input
     * @return true or false depending on if string is valid or not
     */
    private static boolean validateInput(String input){
        if (input == null || input.isEmpty()){
            return false;
        }

        input = input.trim();

        return input.length() == 1 && Character.isAlphabetic(input.charAt(0));
    }


    private static String readStringInternal(){

        try {
            return reader.readLine();
        } catch (IOException ioe){
            System.err.println("There was an input error" + ioe.getMessage());
            return null;
        }
    }
}
