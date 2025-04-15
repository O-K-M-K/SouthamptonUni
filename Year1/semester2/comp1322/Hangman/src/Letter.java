public class Letter {
    private final char letter;
    private boolean guessed = false;

    public Letter(char letter){
        this.letter = letter;
    }

    public char getValue(){
        return letter;
    }

    public boolean isGuessed(){
        return guessed;
    }

    public void guess(){
        this.guessed = true;
    }

}
