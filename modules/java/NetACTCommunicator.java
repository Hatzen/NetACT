/**
 * Sends and recieves states to the mother process.
 */
public class NetACTCommunicator
{
    private static final String prefix = "**//**NetACTCommunicator**START**";
    private static final String postfix = "**END**NetACTCommunicator**//**";

    /**
     * Send current state to the mother process Programm.
     * @param state a String representing the current state of this Program.
     */
    public static void sendState(String state) {
      System.err.println(getUniqueString( state ));
    }


    public static void waitForState(String state) {
      Scanner s = new Scanner(System.in);
      while(!s.readLine().contains(getUniqueString(state)) ) { }
    }

    public static void waitAllForState(String state) {
        // https://stackoverflow.com/questions/1323408/get-a-list-of-all-threads-currently-running-in-java
        Set<Thread> threadSet = Thread.getAllStackTraces().keySet();
        Thread[] threadArray = threadSet.toArray(new Thread[threadSet.size()]);

        for (Thread t : threadArray) {
            if (t != Thread.currentThread()) {
                t.suspend();
            }
        }

        waitForState(state);

        for (Thread t : threadArray) {
            if (t != Thread.currentThread()) {
                t.resume();
            }
        }

    }

    private static String getUniqueString(String state) {
        return prefix + state + postfix;
    }
}