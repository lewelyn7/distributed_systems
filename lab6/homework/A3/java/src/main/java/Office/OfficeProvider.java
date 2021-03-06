//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.5
//
// <auto-generated>
//
// Generated from file `Office.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

package Office;

public interface OfficeProvider extends com.zeroc.Ice.Object
{
    int getDrivingLicense(String who, DrivingLicenseType DrivingType, String examResult, com.zeroc.Ice.Current current);

    int getZUSInfo(String who, String nip, com.zeroc.Ice.Current current);

    int getBuildingPermit(String who, String where, int size, com.zeroc.Ice.Current current);

    void listen(String who, OfficeListenerPrx officeListener, com.zeroc.Ice.Current current);

    /** @hidden */
    static final String[] _iceIds =
    {
        "::Ice::Object",
        "::Office::OfficeProvider"
    };

    @Override
    default String[] ice_ids(com.zeroc.Ice.Current current)
    {
        return _iceIds;
    }

    @Override
    default String ice_id(com.zeroc.Ice.Current current)
    {
        return ice_staticId();
    }

    static String ice_staticId()
    {
        return "::Office::OfficeProvider";
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_getDrivingLicense(OfficeProvider obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
    {
        com.zeroc.Ice.Object._iceCheckMode(null, current.mode);
        com.zeroc.Ice.InputStream istr = inS.startReadParams();
        String iceP_who;
        DrivingLicenseType iceP_DrivingType;
        String iceP_examResult;
        iceP_who = istr.readString();
        iceP_DrivingType = DrivingLicenseType.ice_read(istr);
        iceP_examResult = istr.readString();
        inS.endReadParams();
        int ret = obj.getDrivingLicense(iceP_who, iceP_DrivingType, iceP_examResult, current);
        com.zeroc.Ice.OutputStream ostr = inS.startWriteParams();
        ostr.writeInt(ret);
        inS.endWriteParams(ostr);
        return inS.setResult(ostr);
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_getZUSInfo(OfficeProvider obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
    {
        com.zeroc.Ice.Object._iceCheckMode(null, current.mode);
        com.zeroc.Ice.InputStream istr = inS.startReadParams();
        String iceP_who;
        String iceP_nip;
        iceP_who = istr.readString();
        iceP_nip = istr.readString();
        inS.endReadParams();
        int ret = obj.getZUSInfo(iceP_who, iceP_nip, current);
        com.zeroc.Ice.OutputStream ostr = inS.startWriteParams();
        ostr.writeInt(ret);
        inS.endWriteParams(ostr);
        return inS.setResult(ostr);
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_getBuildingPermit(OfficeProvider obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
    {
        com.zeroc.Ice.Object._iceCheckMode(null, current.mode);
        com.zeroc.Ice.InputStream istr = inS.startReadParams();
        String iceP_who;
        String iceP_where;
        int iceP_size;
        iceP_who = istr.readString();
        iceP_where = istr.readString();
        iceP_size = istr.readInt();
        inS.endReadParams();
        int ret = obj.getBuildingPermit(iceP_who, iceP_where, iceP_size, current);
        com.zeroc.Ice.OutputStream ostr = inS.startWriteParams();
        ostr.writeInt(ret);
        inS.endWriteParams(ostr);
        return inS.setResult(ostr);
    }

    /**
     * @hidden
     * @param obj -
     * @param inS -
     * @param current -
     * @return -
    **/
    static java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceD_listen(OfficeProvider obj, final com.zeroc.IceInternal.Incoming inS, com.zeroc.Ice.Current current)
    {
        com.zeroc.Ice.Object._iceCheckMode(null, current.mode);
        com.zeroc.Ice.InputStream istr = inS.startReadParams();
        String iceP_who;
        OfficeListenerPrx iceP_officeListener;
        iceP_who = istr.readString();
        iceP_officeListener = OfficeListenerPrx.uncheckedCast(istr.readProxy());
        inS.endReadParams();
        obj.listen(iceP_who, iceP_officeListener, current);
        return inS.setResult(inS.writeEmptyParams());
    }

    /** @hidden */
    final static String[] _iceOps =
    {
        "getBuildingPermit",
        "getDrivingLicense",
        "getZUSInfo",
        "ice_id",
        "ice_ids",
        "ice_isA",
        "ice_ping",
        "listen"
    };

    /** @hidden */
    @Override
    default java.util.concurrent.CompletionStage<com.zeroc.Ice.OutputStream> _iceDispatch(com.zeroc.IceInternal.Incoming in, com.zeroc.Ice.Current current)
        throws com.zeroc.Ice.UserException
    {
        int pos = java.util.Arrays.binarySearch(_iceOps, current.operation);
        if(pos < 0)
        {
            throw new com.zeroc.Ice.OperationNotExistException(current.id, current.facet, current.operation);
        }

        switch(pos)
        {
            case 0:
            {
                return _iceD_getBuildingPermit(this, in, current);
            }
            case 1:
            {
                return _iceD_getDrivingLicense(this, in, current);
            }
            case 2:
            {
                return _iceD_getZUSInfo(this, in, current);
            }
            case 3:
            {
                return com.zeroc.Ice.Object._iceD_ice_id(this, in, current);
            }
            case 4:
            {
                return com.zeroc.Ice.Object._iceD_ice_ids(this, in, current);
            }
            case 5:
            {
                return com.zeroc.Ice.Object._iceD_ice_isA(this, in, current);
            }
            case 6:
            {
                return com.zeroc.Ice.Object._iceD_ice_ping(this, in, current);
            }
            case 7:
            {
                return _iceD_listen(this, in, current);
            }
        }

        assert(false);
        throw new com.zeroc.Ice.OperationNotExistException(current.id, current.facet, current.operation);
    }
}
