import java.io.*;
import java.util.List;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
public class Executor
        implements Watcher, Runnable, DataMonitor.DataMonitorListener {
    static Logger logger = Logger.getLogger(Executor.class.getName());
    String znode;
    DataMonitor dm;
    ZooKeeper zk;
    String exec[];
    Process child;

    public Executor(String hostPort, String znode,
                    String exec[]) throws KeeperException, IOException {
        logger.setLevel(Level.INFO);
        this.znode = znode;
        this.exec = exec;
        System.out.println(hostPort);
        zk = new ZooKeeper(hostPort, 3000, this);
        dm = new DataMonitor(zk, znode, null, this);
        CommandsListenerThread cli = new CommandsListenerThread(this);
        cli.start();
        logger.trace("EXECUTOR: created");

    }
    public static void main(String[] args) {
        if (args.length < 3) {
            System.err
                    .println("USAGE: Executor hostPort znode program [args ...]");
            System.exit(2);
        }
        String hostPort = args[0];
        String znode = args[1];
        String exec[] = new String[args.length - 2];

        System.arraycopy(args, 2, exec, 0, exec.length);
        try {
            new Executor(hostPort, znode, exec).run();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public void process(WatchedEvent event) {
        logger.trace(">>>EXECUTOR: new event came");
        logger.info("==============");
        dm.process(event);

    }

    public void run() {
        try {
            synchronized (this) {
                while (!dm.dead) {
                    wait();
                }
            }
        } catch (InterruptedException e) {
        }
    }

    public void closing(int rc) {
        synchronized (this) {
            notifyAll();
        }
    }

    static class StreamWriter extends Thread {
        OutputStream os;

        InputStream is;

        StreamWriter(InputStream is, OutputStream os) {
            this.is = is;
            this.os = os;
            start();
        }

        public void run() {
            byte b[] = new byte[80];
            int rc;
            try {
                while ((rc = is.read(b)) > 0) {
                    os.write(b, 0, rc);
                }
            } catch (IOException e) {
            }

        }
    }

    public void zNodeCreated() {
        if (child == null) {
            try {
                System.out.println("Starting child");
                child = Runtime.getRuntime().exec(exec);
                new StreamWriter(child.getInputStream(), System.out);
                new StreamWriter(child.getErrorStream(), System.err);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void zNodeDeleted() {
        if (child != null) {
            System.out.println("Killing process");
            child.destroy();
            try {
                child.waitFor();
            } catch (InterruptedException e) {
            }
        }
        child = null;
    }



    public void lsTree(String path) throws InterruptedException {
        System.out.println(path);

        List<String> list = null;
        try {
            list = zk.getChildren(path, null);
        } catch (KeeperException e) {
            return;
        }
        // determine whether there is a child node
        if (list.isEmpty() || list == null) {
            logger.trace("child node list is empty");
            return;
        }
        for (String s : list) {
            // determine whether the root directory
            if (path.equals("/")) {
                lsTree(path + s);
            } else {
                lsTree(path + "/" + s);
            }
        }
    }

    static class CommandsListenerThread extends Thread {
        private Executor parent;

        public CommandsListenerThread(Executor executor) {
            this.parent = executor;
        }

        public void run() {
            String thisLine = null;

            try {

                BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                System.out.println("Provide input:");
                while ((thisLine = br.readLine()) != null) {
                    System.out.println("cmd:" + thisLine);
                    parent.lsTree(parent.znode);
                }
            } catch (Exception e) {

            }
        }
    }
}
