public class EasyHangmanGame extends HangmanGame {
    public EasyHangmanGame(){
        super();
        this.difficulty = Difficulty.EASY;
    }

    @Override
    protected int getMaxAttempts(){
        return 10;
    }


    @Override
    protected WordBank getWordBank(String filePath){
        return new EasyWordBank(filePath);
    }
}
