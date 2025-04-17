public enum Difficulty{
    EASY(10), 
    MEDIUM(8), 
    HARD(6);

    private final int maxAttempts;

    Difficulty(int maxAttemps){
        this.maxAttempts = maxAttemps;
    }

    public int getMaxAttempts(){
        return maxAttempts;
    }
}


