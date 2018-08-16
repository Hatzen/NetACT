package netact.modules;

import java.util.Scanner;
import java.util.Set;

/**
 * Sends and recieves states to the parent process.
 */
public class NetACTCommunicator
{
    // Internal attributes to stand out from normal I/O-Data
    private static final String prefix = "**//**NetACTCommunicator**START**";
    private static final String postfix = "**END**NetACTCommunicator**//**";

    /**
     * Send current state to the parent process.
     * @param state a String representing the current state of this Program.
     */
    public static void sendState(String state) {
      System.err.println(getUniqueString( state ));
    }

    /**
     * Will force the current thread to wait until the parent process notifies with
     * the given state.
     * @param state a String representing the state of an external Program.
     */
    public static void waitForState(String state) {
      Scanner s = new Scanner(System.in);
      while(s.hasNextLine() && !s.nextLine().contains(getUniqueString(state)) ) { }
      s.close();
    }

    /**
     * Will force all threads to wait until the parent process notifies with
     * the given state.
     * @param state a String representing the state of an external Program.
     */
    @SuppressWarnings( "deprecation" ) // Only way to hold application state
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