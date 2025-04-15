public class HardHangmanGame extends HangmanGame {
    public HardHangmanGame(){
        super();
        this.difficulty = Difficulty.HARD;
    }

    @Override
    protected int getMaxAttempts(){
        return 6;
    }


    @Override
    protected WordBank getWordBank(String filePath){
        return new HardWordBank(filePath);
    }
}