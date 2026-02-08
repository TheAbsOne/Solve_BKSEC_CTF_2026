import java.util.Scanner;

class Spid3rRev {

  public static String fourth(String t) {
    return t.substring(19) + t.substring(0, 19);
  }

  public static String third(String t) {
    String s = "";
    for (int i = 0; i < t.length(); i++) {
      if (i % 3 == 0)
        s += (char)(t.charAt(i) + (i / 3));
      else if (i % 3 == 2)
        s += (char)(t.charAt(i) + ((i - 2) / 3));
      else
        s += t.charAt(i);
    }
    return s;
  }

  public static String second(String t) {
    String a = t.substring(0, 2);
    String b = t.substring(2, t.length() - 16);
    String c = t.substring(t.length() - 16);
    return c + b + a;
  }

  public static String first(String t) {
    int[] adj = {
      -11,
      34,
      -28,
      -8,
      -57,
      -8,
      2,
      3,
      5,
      -17,
      -13,
      -18,
      -53,
      -5,
      0,
      3,
      -19,
      -16,
      -12,
      -6,
      -48,
      10,
      7,
      -19,
      -4,
      -1,
      -67,
      -19,
      -15,
      9,
      -47,
      -14,
      -8,
      -27,
      3,
      -19,
      3,
      -59,
      5,
      -30,
      8,
      33,
      22,
      -6,
      -50,
      0
    };
    String s = "";
    for (int i = 0; i < t.length(); i++)
      s += (char)(t.charAt(i) + adj[i]);
    return s;
  }

  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
    String flag = in.nextLine();
    String match = "Deim(yobzoRoA`m\u0089`ESf;xmOkh ]g}8VjFw[x-tG\u008dlaVCr";
    if (flag.length() == 46 && first(second(third(fourth(flag)))).equals(match))
      System.out.println("Congratulations!!!!!!!!, Access Granted");
    else
      System.out.println("Access Denied! Please try again!");
    in.close();
  }
}