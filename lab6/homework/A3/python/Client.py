import Ice
import Office
import logging
import sys
import signal
import argparse
class OfficeListenerI(Office.OfficeListener):
    def notify(self, result, context):
        logging.debug("notified")
        print(f"case id:{result.id} positive: {result.positive}")
        return True
        


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Office client program")
    parser.add_argument('--who', dest='who', required=True)
    parser.add_argument('--type', dest='type', choices=['zus','driving','building','listen'], required=True)
    parser.add_argument('--no-listen', dest='no_listen', action='store_true')
    parser.add_argument('params', type=str, nargs='*')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    with Ice.initialize(['--Ice.ThreadPool.Client.Size=2', '--Ice.ThreadPool.Server.Size=2']) as communicator:
        def signal_handler(sig, frame):
            print('You pressed Ctrl+C!')
            communicator.shutdown()
            communicator.destroy()
        signal.signal(signal.SIGINT, signal_handler)



        base = communicator.stringToProxy("SimpleOfficeAdapter:default -p 10000")
        office = Office.OfficeProviderPrx.checkedCast(base)
        case_id = None
        if not office:
            raise RuntimeError("Invalid proxy")
        if args.type == 'zus':
            case_id = office.getZUSInfo(args.who, *args.params)
        elif args.type == 'driving':
            case_id = office.getDrivingLicense(args.who, *args.params)
        elif args.type == 'building':
            case_id = office.getBuildingPermit(args.who, *args.params)
        elif args.type == 'listen':
            pass

        if case_id != None:
            print(f"case id: {case_id}")
        # office.getDrivingLicense("Johnny", "B2", "positive 23/43")
        if not args.no_listen:
            adapter = communicator.createObjectAdapter("")
            cbPrx = Office.OfficeListenerPrx.uncheckedCast(adapter.addWithUUID(OfficeListenerI()))
            office.ice_getCachedConnection().setAdapter(adapter)
            office.listen(args.who, cbPrx)
            communicator.waitForShutdown()
