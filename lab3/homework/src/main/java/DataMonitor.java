
import java.util.List;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.zookeeper.*;
import org.apache.zookeeper.AsyncCallback.StatCallback;
import org.apache.zookeeper.KeeperException.Code;
import org.apache.zookeeper.data.Stat;

public class DataMonitor implements StatCallback, AsyncCallback.Children2Callback {

    Logger logger = Logger.getLogger(DataMonitor.class.getName());

    ZooKeeper zk;

    String znode;

    boolean dead;

    DataMonitorListener listener;


    public DataMonitor(ZooKeeper zk, String znode, Watcher chainedWatcher,
                       DataMonitorListener listener) {
        this.zk = zk;
        this.znode = znode;
        this.listener = listener;
        zk.exists(znode, true, this, null);
        zk.getChildren(znode, true, this, null);
        logger.setLevel(Level.INFO);

    }

    @Override
    public void processResult(int rc, String path, Object ctx, List<String> children, Stat stat) {
        logger.trace("DATAMONITOR: get children completed; rc=" + rc );
        if(rc != 0){
            return;
        }
        System.out.println("node has " + children.size() + " children");
        children.forEach(c -> System.out.println("\t>"+c));
    }


    public interface DataMonitorListener {
        void zNodeCreated();
        void zNodeDeleted();
        void closing(int rc);
    }

    public void process(WatchedEvent event) {
        logger.trace("DATAMONITOR: event came");
        String path = event.getPath();
        if (event.getType() == Watcher.Event.EventType.None) {
            logger.info("event type none");
            switch (event.getState()) {
                case SyncConnected:
                    break;
                case Expired:
                    dead = true;
                    listener.closing(KeeperException.Code.SessionExpired);
                    break;
            }
        } else if (event.getType() == Watcher.Event.EventType.NodeCreated){
            logger.info("event type: znode created");
            zk.exists(znode, true, this, null);
            zk.getChildren(znode, true, this, null);
            listener.zNodeCreated();
        } else if (event.getType() == Watcher.Event.EventType.NodeChildrenChanged){
            logger.info("event type: node children changed");
            zk.getChildren(znode, true, this, null);

        } else if (event.getType() == Watcher.Event.EventType.NodeDeleted){
            logger.info("event type: znode deleted");
            zk.exists(znode, true, this, null);
            listener.zNodeDeleted();

        }
    }

    public void processResult(int rc, String path, Object ctx, Stat stat) {
        logger.trace("DATAMONITOR: exists completed; rc=" + rc );
        boolean exists;
        switch (rc) {
            case Code.SessionExpired:
            case Code.NoAuth:
                dead = true;
                listener.closing(rc);
                return;
        }

    }


}
