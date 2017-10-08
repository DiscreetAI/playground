package data.shark.util;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by ferdows on 6/27/17.
 */

public class OngoSettings {

    /**
     * Start constants
     */

    // For Shared Preferences
    public static final String GROUP_NAME = "group.life.ongo.data.shark.core";
    public static final String SYNC_TOKENS_KEY = GROUP_NAME + ".SYNC_TOKENS_KEY";
    public static final String PRODUCTION_AUTHENTICATION_SERVER_BASE_URL = "https://dev.ongo.life";
    public static final String DEVELOPMENT_AUTHENTICATION_SERVER_BASE_URL = "https://dev.ongo.life";
    public static final String LOCAL_AUTHENTICATION_SERVER_BASE_URL = "http://127.0.0.1:9000";
    public static final String LAST_SYNC_TOKEN = "LAST_SYNC_TOKEN";
    public static final String SERVER_BASE_URL = "SERVER_BASE_URL";
    public static final String LAST_FORCED_SYNC_KEY = "LAST_FORCED_SYNC_KEY";
    public static final String LAST_FORCED_SYNC_VALUE = "REALM_SCHEMA_1";
    private static final String LOG_TAG = "OngoSettings";

    /**
     * End constants
     */
    /**
     * Start data members
     */

    // Singleton
    private static OngoSettings instance;

    private boolean firstTimeUser;

    private String cachedServerBaseURL;

    private SharedPreferences syncTokens;
    private SharedPreferences sharedDefaults;

    // Singleton initializer
    // DO NOT MAKE PUBLIC
    private OngoSettings(Context context) {
        if (context != null) {
            syncTokens = context.getSharedPreferences(SYNC_TOKENS_KEY, Context.MODE_PRIVATE);
            sharedDefaults = context.getSharedPreferences(GROUP_NAME, Context.MODE_PRIVATE);
        }
    }

    /**
     * End data members
     */

    // Singleton getter
    public static OngoSettings getInstance() {
        return instance;
    }

    private static synchronized OngoSettings getSync() {
        return instance;
    }

    public static void initialize(Context context) {
        instance = new OngoSettings(context);
    }

    public static String getLastForcedSyncValue() {
        SharedPreferences sharedDefaults = instance.sharedDefaults;
        return sharedDefaults.getString(LAST_FORCED_SYNC_KEY, null);
    }

    public static void setLastForcedSyncValue(String value) {
        SharedPreferences.Editor sharedDefaultsEditor = instance.sharedDefaults.edit();
        sharedDefaultsEditor.putString(LAST_FORCED_SYNC_KEY, value);
        sharedDefaultsEditor.commit();
    }

    public static boolean needsForcedSync() {
        return (getLastForcedSyncValue() != LAST_FORCED_SYNC_VALUE);
    }

    public static void updateLastForcedSyncValue() {
        setLastForcedSyncValue(LAST_FORCED_SYNC_VALUE);
    }

    public static String getServerBaseURL(boolean useCache) {
        // If it's cached -- return the cached version
        // This prevents any unexpected behavior if the setting is changed
        // while running the app. Users will have to force quit the app for the
        // new URL to take effect.
        if (useCache && OngoSettings.instance.cachedServerBaseURL != null) {
            return OngoSettings.instance.cachedServerBaseURL;
        }

        // Shared preferences
        SharedPreferences sharedDefaults = instance.sharedDefaults;
        SharedPreferences.Editor sharedDefaultsEditor = sharedDefaults.edit();

        String baseURL = sharedDefaults.getString(SERVER_BASE_URL, null);
        if (baseURL == null) {
            // default to production server
            if (useCache) {
                instance.cachedServerBaseURL = PRODUCTION_AUTHENTICATION_SERVER_BASE_URL;
            }
            return PRODUCTION_AUTHENTICATION_SERVER_BASE_URL;
        }

        // check for invalid URL (maybe the base URL changed from previous version?)
        if (baseURL != PRODUCTION_AUTHENTICATION_SERVER_BASE_URL &&
                baseURL != DEVELOPMENT_AUTHENTICATION_SERVER_BASE_URL &&
                baseURL != LOCAL_AUTHENTICATION_SERVER_BASE_URL) {
            Log.d(LOG_TAG, "Reset server base URL: " + PRODUCTION_AUTHENTICATION_SERVER_BASE_URL);
            sharedDefaultsEditor.remove(SERVER_BASE_URL);
            sharedDefaultsEditor.commit();

            if (useCache) {
                instance.cachedServerBaseURL = PRODUCTION_AUTHENTICATION_SERVER_BASE_URL;
            }
            return PRODUCTION_AUTHENTICATION_SERVER_BASE_URL;
        }

        // Cache the URL
        if (useCache) {
            OngoSettings.instance.cachedServerBaseURL = baseURL;
        }
        return baseURL;
    }

    public static String getServerBaseURL() {
        return getServerBaseURL(true);
    }

    public static String getServerHostName() {
        String baseUrl = getServerBaseURL();
        if (baseUrl == null) {
            return null;
        }

        try {
            URL url = new URL(baseUrl);
            String hostname = url.getHost();
            if (hostname == null) {
                return null;
            }

            if (hostname.startsWith("127.0.0.1")) {
                return "localhost";
            } else {
                return hostname;
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }

        return null;
    }

    public void clearSyncToken() {
        String str = "";
        SharedPreferences.Editor syncTokensEditor = syncTokens.edit();
        syncTokensEditor.putString(LAST_SYNC_TOKEN, str);
        syncTokensEditor.commit();
    }

    public String getLastSyncTokenForUser(String userId, String syncType) {
        String defaultToken = "0";
        if (userId == null) {
            return defaultToken;
        }

        String host = getServerHostName();
        if (host == null) {
            host = "localhost";
        }

        String key = host + "|" + userId + "|" + syncType;

        String syncToken = syncTokens.getString(key, null);
        if (syncToken != null) {
            return syncToken;
        }

        // default
        return defaultToken;
    }

    public void setLastSyncTokenForUser(String userId, String syncType, String syncToken) {
        if (userId == null) {
            return;
        }

        String host = getServerHostName();
        if (host == null) {
            host = "localhost";
        }

        String key = host + "|" + userId + "|" + syncType;

        SharedPreferences.Editor syncTokensEditor = syncTokens.edit();
        syncTokensEditor.putString(key, syncToken);
        syncTokensEditor.commit();
    }

}
