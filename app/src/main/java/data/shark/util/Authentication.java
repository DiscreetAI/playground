package data.shark.util;

import android.app.Activity;
import android.content.Intent;
import android.util.Log;

import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.login.LoginManager;
import com.facebook.login.LoginResult;
import com.google.gson.ExclusionStrategy;
import com.google.gson.FieldAttributes;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import io.reactivex.Observable;
import io.realm.RealmObject;
import data.shark.activities.login.LandingActivity;
import data.shark.models.OGObject;
import data.shark.models.OGObjectSerializer;
import data.shark.models.OGUser;
import data.shark.models.OGUserSerializer;
import data.shark.services.AuthService;
import data.shark.services.ServiceBodies.AuthCredentials;
import data.shark.services.ServiceBodies.AuthFacebookCredentials;
import data.shark.services.ServiceBodies.AuthResponse;
import data.shark.services.ServiceBodies.AuthSignupParameters;
import data.shark.services.ServiceBodies.UserProfile;
import data.shark.services.UserService;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;

public class Authentication {
    private static final String SERVER_BASE_URL = "https://app.ongo.life";
    private CallbackManager callbackManager;
    // Instance Variables
    private Retrofit retrofit;
    private OGUser currentUser;
    private String currentUserId;
    private String authToken;
    private OGUser profileUser;

    private Authentication() {
        this.currentUser = null;
        this.currentUserId = null;
        this.authToken = null;
        initialize();
    }

    public static Authentication getInstance() {
        return AuthenticationHolder.INSTANCE;
    }

    public static Retrofit retrofit() {
        return getInstance().getRetrofit();
    }

    public static AuthService authService() {
        return retrofit().create(AuthService.class);
    }

    public static UserService userService() {
        return retrofit().create(UserService.class);
    }

    private void initialize() {
        // Set-up OkHttp to use the AuthenticationInterceptor (inserts auth token when logged in)
        OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
        httpClient.addInterceptor(new AuthenticationInterceptor());
        OkHttpClient client = httpClient.build();

        // For GSON/Realm compatibility
        ExclusionStrategy exclusionStrategy = new ExclusionStrategy() {
            @Override
            public boolean shouldSkipField(FieldAttributes f) {
                return f.getDeclaringClass().equals(RealmObject.class);
            }

            @Override
            public boolean shouldSkipClass(Class<?> clazz) {
                return false;
            }
        };

        // Register GSON serializers here
        Gson gson = new GsonBuilder()
                .setExclusionStrategies(exclusionStrategy)
                .registerTypeAdapter(OGObject.class, new OGObjectSerializer())
                .registerTypeAdapter(OGUser.class, new OGUserSerializer())
                .create();

        // Set up the retrofit builder
        Retrofit builder = new Retrofit.Builder()
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .addConverterFactory(GsonConverterFactory.create(gson))
                .baseUrl(SERVER_BASE_URL)
                .client(client)
                .build();
        this.retrofit = builder;
    }

    public Retrofit getRetrofit() {
        return retrofit;
    }

    public OGUser getCurrentUser() {
        return this.currentUser;
    }

    public void setCurrentUser(OGUser value) {
        currentUser = value;
        currentUserId = value._id;
    }

    public String getCurrentUserId() {
        return this.currentUserId;
    }

    public String getAuthToken() {
        return this.authToken;
    }

    public void setAuthToken(String newToken) {
        this.authToken = newToken;
    }

//    public Observable<AuthResponse> loginWithStoredCredentials() {
//        AuthCredentials credentials = SecureSettings.getAuthCredentials();
//        AuthService auth = authService();
//        return auth.loginWithCredentials(credentials);
//    }

    public Observable<AuthResponse> loginWithCredentials(AuthCredentials credentials) {
        AuthService auth = authService();
        return auth.loginWithCredentials(credentials);
    }

    public Observable<AuthResponse> loginWithFacebook(AuthFacebookCredentials credentials) {
        AuthService auth = authService();
        return auth.loginWithFacebook(credentials);
    }

    public Observable<AuthResponse> signupWithParameters(AuthSignupParameters parameters) {
        AuthService auth = authService();
        return auth.signupUser(parameters);
    }

    public Observable<OGUser> updateProfile(String userId, UserProfile profile) {
        UserService userService = userService();
        return userService.updateUserProfile(userId, profile);
    }

    public synchronized void handleLogin(AuthResponse response) {
        if (response.user != null && response.user._id != null && response.token != null) {
            Log.i("Authentication", "Logged in as " + response.user);
            this.currentUserId = response.user._id;
            this.currentUser = response.user;
//            Realm realm = Realm.getDefaultInstance();
////            RealmResults<OGSyncRecord> obj = realm.where(OGSyncRecord.class).equalTo("objType", "OGUser").equalTo("owner", currentUserId).findAll();
//            RealmResults<OGSyncRecord> obj = realm.where(OGSyncRecord.class).findAll();
//            if (obj.first() != null) {
//                Log.v("Authentication", "founduser");
////                this.currentUser = obj.first();
//            }
            this.authToken = response.token;
        }
    }

    public void logout(final Activity activity) {
        this.currentUser = null;
        this.currentUserId = null;
        this.authToken = null;
        callbackManager = CallbackManager.Factory.create();

        LoginManager.getInstance().logOut();
        LoginManager.getInstance().registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                Intent logoutIntent = new Intent(activity, LandingActivity.class);
                logoutIntent.putExtra("autoLogin", true);
                activity.startActivity(logoutIntent);
            }

            @Override
            public void onCancel() {

            }

            @Override
            public void onError(FacebookException error) {

            }
        });
        Intent logoutIntent = new Intent(activity, LandingActivity.class);
        logoutIntent.putExtra("autoLogin", true);
        activity.startActivity(logoutIntent);
    }

    private static class AuthenticationHolder {
        private static final Authentication INSTANCE = new Authentication();
    }

}
