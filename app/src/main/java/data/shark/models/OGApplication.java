package data.shark.models;

import android.app.Application;
import android.content.Context;

public class OGApplication extends Application {

    private static Context context;

    public static Context getAppContext() {
        return OGApplication.context;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        OGApplication.context = getApplicationContext();
    }

}
