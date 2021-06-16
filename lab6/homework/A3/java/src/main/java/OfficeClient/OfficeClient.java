package OfficeClient;
import Office.*;
import com.zeroc.Ice.*;
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.impl.action.StoreTrueArgumentAction;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.ArgumentType;
import net.sourceforge.argparse4j.inf.Namespace;

import java.io.IOException;
import java.lang.Exception;
import java.lang.reflect.Array;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.concurrent.CompletableFuture;
import java.util.logging.*;
import java.util.logging.Logger;

class OfficeListenerI implements OfficeListener {

    @Override
    public boolean _notify(Result result, Current context){
        System.out.println("case " + result.id + " resolved with status " + result.positive + " time elapsed: " + result.timeElapsed + "s");
        return true;
    }

}


public class OfficeClient {
    protected static final Logger logger = Logger.getLogger("main"); //java.util.logging.Logger
    public static void main(String[] args){
        logger.setUseParentHandlers(false);
        ConsoleHandler handler = new ConsoleHandler();

        logger.addHandler(handler);


        try {
            Communicator communicator = Util.initialize(args);
            ObjectPrx server = communicator.stringToProxy("SimpleOfficeAdapter:default -p 10000");
            OfficeProviderPrx office = OfficeProviderPrx.checkedCast(server);

            ObjectAdapter adapter = communicator.createObjectAdapter("");
            OfficeListenerPrx officeListener = OfficeListenerPrx.uncheckedCast(adapter.addWithUUID(new OfficeListenerI()));
            adapter.activate();
            office.ice_getConnection().setAdapter(adapter);

            final ArgumentParser argumentParser =
                    ArgumentParsers.newArgumentParser("Main", true);
            argumentParser.addArgument("-t", "--type")
                    .dest("type")
                    .required(true)
                    .choices(new ArrayList<String>(Arrays.asList("ZUS", "driving", "building", "listen")))
                    .help("type of case");
            argumentParser.addArgument("-w", "--who")
                    .dest("who")
                    .type(String.class)
                    .required(true)
                    .help("name of Office client");
            argumentParser.addArgument("params")
                    .type(String.class)
                    .nargs("*");
            argumentParser.addArgument("--no-listen")
                    .dest("no_listen")
                    .action(new StoreTrueArgumentAction());
            try {

                final Namespace response = argumentParser.parseArgs(args);
                int caseId = -1;
                String caseType = response.getString("type");
                if (caseType.equals("ZUS")) {
                    if (response.getList("params").size() != 1) {
                        throw new ArgumentParserException("wrong params; NIP is required", argumentParser);
                    }
                    String nip = (String) response.getList("params").get(0);
                    logger.info("Sending zus request");
                    logger.log(Level.INFO, "NIP: {0}", nip);
                    caseId = office.getZUSInfo(response.getString("who"), nip);
                } else if (caseType.equals("driving")) {
                    if (response.getList("params").size() != 2) {
                        throw new ArgumentParserException("wrong params; DRIVING_TYPE and EXAM_RESULT are required", argumentParser);
                    }

                    String drivingLicenseTypeString = (String) response.getList("params").get(0);
                    String exam =  (String) response.getList("params").get(1);
                    DrivingLicenseType drivingLicenseType = DrivingLicenseType.valueOf(drivingLicenseTypeString);
                    logger.info("Sending driving license request");
                    logger.log(Level.INFO, "exam: {0}", exam);
                    logger.log(Level.INFO, "type: {0}", drivingLicenseTypeString);
                    caseId = office.getDrivingLicense(response.getString("who"),
                            drivingLicenseType, exam);

                } else if (caseType.equals("building")) {
                    if (response.getList("params").size() != 2) {
                        throw new ArgumentParserException("wrong params; WHERE and SIZE are required", argumentParser);
                    }
                    String where = (String) response.getList("params").get(0);
                    Integer size = Integer.parseInt((String) response.getList("params").get(1));
                    logger.info("Sending building request");
                    logger.log(Level.INFO, "where: {0}", where);
                    logger.log(Level.INFO, "size: {0}", size);

                    caseId = office.getBuildingPermit(response.getString("who"),
                            where, size);
                } else if (caseType.equals("listen")) {
                }
                if (caseId != -1) {
                    System.out.println("returned case id: " + caseId);
                }
                if (!response.getBoolean("no_listen")) {
                    logger.info("listen for results...");
                    office.listen(response.getString("who"), officeListener);
                } else {
                    communicator.destroy();
                }
            } catch (ArgumentParserException e) {
                System.out.println("Parsing error");
                System.out.println(e.getMessage());
                communicator.destroy();
            }
        }catch (ConnectFailedException|ConnectionLostException e){

            System.out.println("Couldn't connect to remote office server");
            System.exit(0);
        }
    }
}
