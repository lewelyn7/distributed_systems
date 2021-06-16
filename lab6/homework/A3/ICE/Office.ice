module Office{  
    struct Result{
        bool positive;
        int id;
        long timeElapsed;
    };
    interface OfficeListener{
        bool notify(Result result);
    };
    
    enum DrivingLicenseType { B2, B1, C, E};

    interface OfficeProvider{
        int getDrivingLicense(string who, DrivingLicenseType DrivingType, string examResult);
        int getZUSInfo(string who, string nip);
        int getBuildingPermit(string who, string where, int size);
        void listen(string who, OfficeListener *officeListener);
    };

}