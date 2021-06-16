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

public interface OfficeProviderPrx extends com.zeroc.Ice.ObjectPrx
{
    default int getDrivingLicense(String who, DrivingLicenseType DrivingType, String examResult)
    {
        return getDrivingLicense(who, DrivingType, examResult, com.zeroc.Ice.ObjectPrx.noExplicitContext);
    }

    default int getDrivingLicense(String who, DrivingLicenseType DrivingType, String examResult, java.util.Map<String, String> context)
    {
        return _iceI_getDrivingLicenseAsync(who, DrivingType, examResult, context, true).waitForResponse();
    }

    default java.util.concurrent.CompletableFuture<java.lang.Integer> getDrivingLicenseAsync(String who, DrivingLicenseType DrivingType, String examResult)
    {
        return _iceI_getDrivingLicenseAsync(who, DrivingType, examResult, com.zeroc.Ice.ObjectPrx.noExplicitContext, false);
    }

    default java.util.concurrent.CompletableFuture<java.lang.Integer> getDrivingLicenseAsync(String who, DrivingLicenseType DrivingType, String examResult, java.util.Map<String, String> context)
    {
        return _iceI_getDrivingLicenseAsync(who, DrivingType, examResult, context, false);
    }

    /**
     * @hidden
     * @param iceP_who -
     * @param iceP_DrivingType -
     * @param iceP_examResult -
     * @param context -
     * @param sync -
     * @return -
     **/
    default com.zeroc.IceInternal.OutgoingAsync<java.lang.Integer> _iceI_getDrivingLicenseAsync(String iceP_who, DrivingLicenseType iceP_DrivingType, String iceP_examResult, java.util.Map<String, String> context, boolean sync)
    {
        com.zeroc.IceInternal.OutgoingAsync<java.lang.Integer> f = new com.zeroc.IceInternal.OutgoingAsync<>(this, "getDrivingLicense", null, sync, null);
        f.invoke(true, context, null, ostr -> {
                     ostr.writeString(iceP_who);
                     DrivingLicenseType.ice_write(ostr, iceP_DrivingType);
                     ostr.writeString(iceP_examResult);
                 }, istr -> {
                     int ret;
                     ret = istr.readInt();
                     return ret;
                 });
        return f;
    }

    default int getZUSInfo(String who, String nip)
    {
        return getZUSInfo(who, nip, com.zeroc.Ice.ObjectPrx.noExplicitContext);
    }

    default int getZUSInfo(String who, String nip, java.util.Map<String, String> context)
    {
        return _iceI_getZUSInfoAsync(who, nip, context, true).waitForResponse();
    }

    default java.util.concurrent.CompletableFuture<java.lang.Integer> getZUSInfoAsync(String who, String nip)
    {
        return _iceI_getZUSInfoAsync(who, nip, com.zeroc.Ice.ObjectPrx.noExplicitContext, false);
    }

    default java.util.concurrent.CompletableFuture<java.lang.Integer> getZUSInfoAsync(String who, String nip, java.util.Map<String, String> context)
    {
        return _iceI_getZUSInfoAsync(who, nip, context, false);
    }

    /**
     * @hidden
     * @param iceP_who -
     * @param iceP_nip -
     * @param context -
     * @param sync -
     * @return -
     **/
    default com.zeroc.IceInternal.OutgoingAsync<java.lang.Integer> _iceI_getZUSInfoAsync(String iceP_who, String iceP_nip, java.util.Map<String, String> context, boolean sync)
    {
        com.zeroc.IceInternal.OutgoingAsync<java.lang.Integer> f = new com.zeroc.IceInternal.OutgoingAsync<>(this, "getZUSInfo", null, sync, null);
        f.invoke(true, context, null, ostr -> {
                     ostr.writeString(iceP_who);
                     ostr.writeString(iceP_nip);
                 }, istr -> {
                     int ret;
                     ret = istr.readInt();
                     return ret;
                 });
        return f;
    }

    default int getBuildingPermit(String who, String where, int size)
    {
        return getBuildingPermit(who, where, size, com.zeroc.Ice.ObjectPrx.noExplicitContext);
    }

    default int getBuildingPermit(String who, String where, int size, java.util.Map<String, String> context)
    {
        return _iceI_getBuildingPermitAsync(who, where, size, context, true).waitForResponse();
    }

    default java.util.concurrent.CompletableFuture<java.lang.Integer> getBuildingPermitAsync(String who, String where, int size)
    {
        return _iceI_getBuildingPermitAsync(who, where, size, com.zeroc.Ice.ObjectPrx.noExplicitContext, false);
    }

    default java.util.concurrent.CompletableFuture<java.lang.Integer> getBuildingPermitAsync(String who, String where, int size, java.util.Map<String, String> context)
    {
        return _iceI_getBuildingPermitAsync(who, where, size, context, false);
    }

    /**
     * @hidden
     * @param iceP_who -
     * @param iceP_where -
     * @param iceP_size -
     * @param context -
     * @param sync -
     * @return -
     **/
    default com.zeroc.IceInternal.OutgoingAsync<java.lang.Integer> _iceI_getBuildingPermitAsync(String iceP_who, String iceP_where, int iceP_size, java.util.Map<String, String> context, boolean sync)
    {
        com.zeroc.IceInternal.OutgoingAsync<java.lang.Integer> f = new com.zeroc.IceInternal.OutgoingAsync<>(this, "getBuildingPermit", null, sync, null);
        f.invoke(true, context, null, ostr -> {
                     ostr.writeString(iceP_who);
                     ostr.writeString(iceP_where);
                     ostr.writeInt(iceP_size);
                 }, istr -> {
                     int ret;
                     ret = istr.readInt();
                     return ret;
                 });
        return f;
    }

    default void listen(String who, OfficeListenerPrx officeListener)
    {
        listen(who, officeListener, com.zeroc.Ice.ObjectPrx.noExplicitContext);
    }

    default void listen(String who, OfficeListenerPrx officeListener, java.util.Map<String, String> context)
    {
        _iceI_listenAsync(who, officeListener, context, true).waitForResponse();
    }

    default java.util.concurrent.CompletableFuture<Void> listenAsync(String who, OfficeListenerPrx officeListener)
    {
        return _iceI_listenAsync(who, officeListener, com.zeroc.Ice.ObjectPrx.noExplicitContext, false);
    }

    default java.util.concurrent.CompletableFuture<Void> listenAsync(String who, OfficeListenerPrx officeListener, java.util.Map<String, String> context)
    {
        return _iceI_listenAsync(who, officeListener, context, false);
    }

    /**
     * @hidden
     * @param iceP_who -
     * @param iceP_officeListener -
     * @param context -
     * @param sync -
     * @return -
     **/
    default com.zeroc.IceInternal.OutgoingAsync<Void> _iceI_listenAsync(String iceP_who, OfficeListenerPrx iceP_officeListener, java.util.Map<String, String> context, boolean sync)
    {
        com.zeroc.IceInternal.OutgoingAsync<Void> f = new com.zeroc.IceInternal.OutgoingAsync<>(this, "listen", null, sync, null);
        f.invoke(false, context, null, ostr -> {
                     ostr.writeString(iceP_who);
                     ostr.writeProxy(iceP_officeListener);
                 }, null);
        return f;
    }

    /**
     * Contacts the remote server to verify that the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param obj The untyped proxy.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    static OfficeProviderPrx checkedCast(com.zeroc.Ice.ObjectPrx obj)
    {
        return com.zeroc.Ice.ObjectPrx._checkedCast(obj, ice_staticId(), OfficeProviderPrx.class, _OfficeProviderPrxI.class);
    }

    /**
     * Contacts the remote server to verify that the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param obj The untyped proxy.
     * @param context The Context map to send with the invocation.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    static OfficeProviderPrx checkedCast(com.zeroc.Ice.ObjectPrx obj, java.util.Map<String, String> context)
    {
        return com.zeroc.Ice.ObjectPrx._checkedCast(obj, context, ice_staticId(), OfficeProviderPrx.class, _OfficeProviderPrxI.class);
    }

    /**
     * Contacts the remote server to verify that a facet of the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param obj The untyped proxy.
     * @param facet The name of the desired facet.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    static OfficeProviderPrx checkedCast(com.zeroc.Ice.ObjectPrx obj, String facet)
    {
        return com.zeroc.Ice.ObjectPrx._checkedCast(obj, facet, ice_staticId(), OfficeProviderPrx.class, _OfficeProviderPrxI.class);
    }

    /**
     * Contacts the remote server to verify that a facet of the object implements this type.
     * Raises a local exception if a communication error occurs.
     * @param obj The untyped proxy.
     * @param facet The name of the desired facet.
     * @param context The Context map to send with the invocation.
     * @return A proxy for this type, or null if the object does not support this type.
     **/
    static OfficeProviderPrx checkedCast(com.zeroc.Ice.ObjectPrx obj, String facet, java.util.Map<String, String> context)
    {
        return com.zeroc.Ice.ObjectPrx._checkedCast(obj, facet, context, ice_staticId(), OfficeProviderPrx.class, _OfficeProviderPrxI.class);
    }

    /**
     * Downcasts the given proxy to this type without contacting the remote server.
     * @param obj The untyped proxy.
     * @return A proxy for this type.
     **/
    static OfficeProviderPrx uncheckedCast(com.zeroc.Ice.ObjectPrx obj)
    {
        return com.zeroc.Ice.ObjectPrx._uncheckedCast(obj, OfficeProviderPrx.class, _OfficeProviderPrxI.class);
    }

    /**
     * Downcasts the given proxy to this type without contacting the remote server.
     * @param obj The untyped proxy.
     * @param facet The name of the desired facet.
     * @return A proxy for this type.
     **/
    static OfficeProviderPrx uncheckedCast(com.zeroc.Ice.ObjectPrx obj, String facet)
    {
        return com.zeroc.Ice.ObjectPrx._uncheckedCast(obj, facet, OfficeProviderPrx.class, _OfficeProviderPrxI.class);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the per-proxy context.
     * @param newContext The context for the new proxy.
     * @return A proxy with the specified per-proxy context.
     **/
    @Override
    default OfficeProviderPrx ice_context(java.util.Map<String, String> newContext)
    {
        return (OfficeProviderPrx)_ice_context(newContext);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the adapter ID.
     * @param newAdapterId The adapter ID for the new proxy.
     * @return A proxy with the specified adapter ID.
     **/
    @Override
    default OfficeProviderPrx ice_adapterId(String newAdapterId)
    {
        return (OfficeProviderPrx)_ice_adapterId(newAdapterId);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the endpoints.
     * @param newEndpoints The endpoints for the new proxy.
     * @return A proxy with the specified endpoints.
     **/
    @Override
    default OfficeProviderPrx ice_endpoints(com.zeroc.Ice.Endpoint[] newEndpoints)
    {
        return (OfficeProviderPrx)_ice_endpoints(newEndpoints);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the locator cache timeout.
     * @param newTimeout The new locator cache timeout (in seconds).
     * @return A proxy with the specified locator cache timeout.
     **/
    @Override
    default OfficeProviderPrx ice_locatorCacheTimeout(int newTimeout)
    {
        return (OfficeProviderPrx)_ice_locatorCacheTimeout(newTimeout);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the invocation timeout.
     * @param newTimeout The new invocation timeout (in seconds).
     * @return A proxy with the specified invocation timeout.
     **/
    @Override
    default OfficeProviderPrx ice_invocationTimeout(int newTimeout)
    {
        return (OfficeProviderPrx)_ice_invocationTimeout(newTimeout);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for connection caching.
     * @param newCache <code>true</code> if the new proxy should cache connections; <code>false</code> otherwise.
     * @return A proxy with the specified caching policy.
     **/
    @Override
    default OfficeProviderPrx ice_connectionCached(boolean newCache)
    {
        return (OfficeProviderPrx)_ice_connectionCached(newCache);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the endpoint selection policy.
     * @param newType The new endpoint selection policy.
     * @return A proxy with the specified endpoint selection policy.
     **/
    @Override
    default OfficeProviderPrx ice_endpointSelection(com.zeroc.Ice.EndpointSelectionType newType)
    {
        return (OfficeProviderPrx)_ice_endpointSelection(newType);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for how it selects endpoints.
     * @param b If <code>b</code> is <code>true</code>, only endpoints that use a secure transport are
     * used by the new proxy. If <code>b</code> is false, the returned proxy uses both secure and
     * insecure endpoints.
     * @return A proxy with the specified selection policy.
     **/
    @Override
    default OfficeProviderPrx ice_secure(boolean b)
    {
        return (OfficeProviderPrx)_ice_secure(b);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the encoding used to marshal parameters.
     * @param e The encoding version to use to marshal request parameters.
     * @return A proxy with the specified encoding version.
     **/
    @Override
    default OfficeProviderPrx ice_encodingVersion(com.zeroc.Ice.EncodingVersion e)
    {
        return (OfficeProviderPrx)_ice_encodingVersion(e);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for its endpoint selection policy.
     * @param b If <code>b</code> is <code>true</code>, the new proxy will use secure endpoints for invocations
     * and only use insecure endpoints if an invocation cannot be made via secure endpoints. If <code>b</code> is
     * <code>false</code>, the proxy prefers insecure endpoints to secure ones.
     * @return A proxy with the specified selection policy.
     **/
    @Override
    default OfficeProviderPrx ice_preferSecure(boolean b)
    {
        return (OfficeProviderPrx)_ice_preferSecure(b);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the router.
     * @param router The router for the new proxy.
     * @return A proxy with the specified router.
     **/
    @Override
    default OfficeProviderPrx ice_router(com.zeroc.Ice.RouterPrx router)
    {
        return (OfficeProviderPrx)_ice_router(router);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for the locator.
     * @param locator The locator for the new proxy.
     * @return A proxy with the specified locator.
     **/
    @Override
    default OfficeProviderPrx ice_locator(com.zeroc.Ice.LocatorPrx locator)
    {
        return (OfficeProviderPrx)_ice_locator(locator);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for collocation optimization.
     * @param b <code>true</code> if the new proxy enables collocation optimization; <code>false</code> otherwise.
     * @return A proxy with the specified collocation optimization.
     **/
    @Override
    default OfficeProviderPrx ice_collocationOptimized(boolean b)
    {
        return (OfficeProviderPrx)_ice_collocationOptimized(b);
    }

    /**
     * Returns a proxy that is identical to this proxy, but uses twoway invocations.
     * @return A proxy that uses twoway invocations.
     **/
    @Override
    default OfficeProviderPrx ice_twoway()
    {
        return (OfficeProviderPrx)_ice_twoway();
    }

    /**
     * Returns a proxy that is identical to this proxy, but uses oneway invocations.
     * @return A proxy that uses oneway invocations.
     **/
    @Override
    default OfficeProviderPrx ice_oneway()
    {
        return (OfficeProviderPrx)_ice_oneway();
    }

    /**
     * Returns a proxy that is identical to this proxy, but uses batch oneway invocations.
     * @return A proxy that uses batch oneway invocations.
     **/
    @Override
    default OfficeProviderPrx ice_batchOneway()
    {
        return (OfficeProviderPrx)_ice_batchOneway();
    }

    /**
     * Returns a proxy that is identical to this proxy, but uses datagram invocations.
     * @return A proxy that uses datagram invocations.
     **/
    @Override
    default OfficeProviderPrx ice_datagram()
    {
        return (OfficeProviderPrx)_ice_datagram();
    }

    /**
     * Returns a proxy that is identical to this proxy, but uses batch datagram invocations.
     * @return A proxy that uses batch datagram invocations.
     **/
    @Override
    default OfficeProviderPrx ice_batchDatagram()
    {
        return (OfficeProviderPrx)_ice_batchDatagram();
    }

    /**
     * Returns a proxy that is identical to this proxy, except for compression.
     * @param co <code>true</code> enables compression for the new proxy; <code>false</code> disables compression.
     * @return A proxy with the specified compression setting.
     **/
    @Override
    default OfficeProviderPrx ice_compress(boolean co)
    {
        return (OfficeProviderPrx)_ice_compress(co);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for its connection timeout setting.
     * @param t The connection timeout for the proxy in milliseconds.
     * @return A proxy with the specified timeout.
     **/
    @Override
    default OfficeProviderPrx ice_timeout(int t)
    {
        return (OfficeProviderPrx)_ice_timeout(t);
    }

    /**
     * Returns a proxy that is identical to this proxy, except for its connection ID.
     * @param connectionId The connection ID for the new proxy. An empty string removes the connection ID.
     * @return A proxy with the specified connection ID.
     **/
    @Override
    default OfficeProviderPrx ice_connectionId(String connectionId)
    {
        return (OfficeProviderPrx)_ice_connectionId(connectionId);
    }

    /**
     * Returns a proxy that is identical to this proxy, except it's a fixed proxy bound
     * the given connection.@param connection The fixed proxy connection.
     * @return A fixed proxy bound to the given connection.
     **/
    @Override
    default OfficeProviderPrx ice_fixed(com.zeroc.Ice.Connection connection)
    {
        return (OfficeProviderPrx)_ice_fixed(connection);
    }

    static String ice_staticId()
    {
        return "::Office::OfficeProvider";
    }
}