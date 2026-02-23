public class Pillars {
    public static int h=0,mh=0; 
    public static void main(String[] args)  {   
        java.util.Scanner scan = new java.util.Scanner (System.in);
        int n = scan.nextInt();
        int a[]=new int[n];     
        for(int i=0;i<n;i++)
        {
            a[i]=scan.nextInt();
            mh+=a[i];
        }
        mh/=2;// the height of the two pillars is the total, then single pillar can't be more than half of total 
        maxHeight(0,0,a,0);
        // if no pillars can be built using the data, this print statement is executed
        System.out.println("Maximum Height Formed with the given Data "+h);     
    }

    public static void maxHeight(int x,int y,int a[],int i)
    {
        if(x==y && x!=0 && x>h)// whether the heights formed are equal or not 
        {
            h=x;
            if(h==mh) // if equal then print and exit the program
            {
                System.out.println("Maximum Height Formed with the given Data "+h);
                System.exit(0);
            }
        }
        if(i<a.length )
        {
            maxHeight(x+a[i],y,a,i+1);
            maxHeight(x,y+a[i],a,i+1);          
        }       
    }
}