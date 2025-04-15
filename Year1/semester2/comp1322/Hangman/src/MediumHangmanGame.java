public class MediumHangmanGame extends HangmanGame {
    public MediumHangmanGame(){
        super();
        this.difficulty = Difficulty.MEDIUM;
    }

    @Override
    protected int getMaxAttempts(){
        return 8;
    }


    @Override
    protected WordBank getWordBank(String filePath){
        return new MediumWordBank(filePath);
    }
}