package data.shark;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.facebook.AccessToken;
import com.facebook.AccessTokenTracker;
import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.GraphRequest;
import com.facebook.appevents.AppEventsLogger;
import com.facebook.login.LoginManager;
import com.facebook.login.LoginResult;
import com.facebook.login.widget.LoginButton;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;

import java.util.Arrays;

import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import data.shark.R;

public class LandingActivity extends AppCompatActivity implements View.OnClickListener {
    AccessToken accessToken;
    AccessTokenTracker accessTokenTracker;
    ProgressBar progressBar;
    private CallbackManager callbackManager;
    private LoginButton fbLoginButton;
    private TextView tagLine;
    private Button loginButton;
    private Button signupButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        AppEventsLogger.activateApp(getApplication());
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_landing);
        accessTokenTracker = new AccessTokenTracker() {
            @Override
            protected void onCurrentAccessTokenChanged(
                    AccessToken oldAccessToken,
                    AccessToken currentAccessToken) {
                // Set the access token using
                // currentAccessToken when it's loaded or set.
            }
        };
        // If the access token is available already assign it.
        accessToken = AccessToken.getCurrentAccessToken();
        boolean autoLogin = getIntent().getBooleanExtra("autoLogin", false);

        // Check for first time launch for credentials
        if (!autoLogin) {
            SecureSettings.checkForFirstTimeRun();
        }
        //UI Components
        tagLine = (TextView) findViewById(R.id.tag_line);
        fbLoginButton = (LoginButton) findViewById(R.id.fb_login_button);
        fbLoginButton.setReadPermissions("email");
        callbackManager = CallbackManager.Factory.create();
        LoginManager.getInstance().logOut();
        if (!autoLogin) {
            LoginManager.getInstance().logInWithReadPermissions(this, Arrays.asList("email", "user_photos", "public_profile"));
            LoginManager.getInstance().registerCallback(callbackManager,
                    new FacebookCallback<LoginResult>() {
                        @Override
                        public void onSuccess(LoginResult loginResults) {

                            GraphRequest request = GraphRequest.newMeRequest(
                                    loginResults.getAccessToken(),
                                    (object, response) -> {
                                        // Application code
                                        Log.v("LoginActivity", response.toString());
                                    });
                            Bundle parameters = new Bundle();
                            parameters.putString("fields", "id,name,email,gender, birthday");
                            request.setParameters(parameters);
                            request.executeAsync();
                            // App code
//                            showProgress(true);
                            Authentication.getInstance()
                                    .loginWithFacebook(new AuthFacebookCredentials(loginResults.getAccessToken()))
                                    .subscribeOn(Schedulers.newThread())
                                    .observeOn(AndroidSchedulers.mainThread())
                                    .subscribe(new Observer<AuthResponse>() {
                                        @Override
                                        public void onSubscribe(Disposable d) {
                                        }

                                        @Override
                                        public void onNext(AuthResponse value) {
                                            // Handle login event for Authentication class
                                            Authentication.getInstance().handleLogin(value);
                                            //track

                                            // fetch my mTracks
                                            TrackService service = DataSource.getTrackService();
                                            // TODO store the API_VERSION somewhere better
                                            service.downloadTrack(Authentication.getInstance().getCurrentUser().mainTrack, 4) // api: 4, limit: 10, page: 1
                                                    .subscribeOn(Schedulers.newThread())
                                                    .observeOn(AndroidSchedulers.mainThread())
                                                    .subscribe(new Observer<OGTrack>() {
                                                        @Override
                                                        public void onSubscribe(Disposable d) {
                                                        }

                                                        @Override
                                                        public void onNext(OGTrack track) {
                                                            TrackEnrollmentManager.addOrReplaceTrack(track);
                                                            Intent intent = new Intent(LandingActivity.this, TabbedActivity.class);
                                                            startActivity(intent);
//                                                            showProgress(false);
                                                            LandingActivity.this.finish();
                                                        }

                                                        @Override
                                                        public void onError(Throwable e) {
                                                            Log.e("Authentication", "Error fetching MyTracks!");
                                                            e.printStackTrace();
                                                        }

                                                        @Override
                                                        public void onComplete() {
                                                        }
                                                    });

                                        }

                                        @Override
                                        public void onError(Throwable e) {
                                            Log.e("hello", "world", e);
                                        }

                                        @Override
                                        public void onComplete() {
                                        }
                                    });
                        }

                        @Override
                        public void onCancel() {

                            Log.e("dd", "this login canceled");

                        }


                        @Override
                        public void onError(FacebookException e) {


                            Log.e("dd", "facebook login failed error");

                        }
                    });
        }
        fbLoginButton.registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                // App code
                showProgress(true);
                Authentication.getInstance()
                        .loginWithFacebook(new AuthFacebookCredentials(loginResult.getAccessToken()))
                        .subscribeOn(Schedulers.newThread())
                        .observeOn(AndroidSchedulers.mainThread())
                        .subscribe(new Observer<AuthResponse>() {
                            @Override
                            public void onSubscribe(Disposable d) {

                            }

                            @Override
                            public void onNext(AuthResponse value) {
                                Authentication.getInstance().handleLogin(value);
                                TrackService service = DataSource.getTrackService();
                                service.downloadTrack(Authentication.getInstance().getCurrentUser().mainTrack, 4) // api: 4, limit: 10, page: 1
                                        .subscribeOn(Schedulers.newThread())
                                        .observeOn(AndroidSchedulers.mainThread())
                                        .subscribe(new Observer<OGTrack>() {
                                            @Override
                                            public void onSubscribe(Disposable d) {
                                            }

                                            @Override
                                            public void onNext(OGTrack track) {
                                                TrackEnrollmentManager.addOrReplaceTrack(track);
                                                Intent intent = new Intent(LandingActivity.this, TabbedActivity.class);
                                                startActivity(intent);
//                                                showProgress(false);
                                                LandingActivity.this.finish();
                                            }

                                            @Override
                                            public void onError(Throwable e) {
                                                Log.e("Authentication", e.toString());
                                                e.printStackTrace();
                                            }

                                            @Override
                                            public void onComplete() {
                                            }
                                        });
                            }

                            @Override
                            public void onError(Throwable e) {
                                Log.e("hello", "world", e);
                            }

                            @Override
                            public void onComplete() {

                            }
                        });
            }

            @Override
            public void onCancel() {
                Log.e("dd", "facebook login canceled");
            }

            @Override
            public void onError(FacebookException exception) {
                Log.e("fb", exception.toString());
                // App code
            }
        });
        signupButton = (Button) findViewById(R.id.signup_button);
        loginButton = (Button) findViewById(R.id.login_button);

        //Set fonts
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] regTextViews = new TextView[]{tagLine, fbLoginButton, signupButton, loginButton};
        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);

        fbLoginButton.setOnClickListener(this);
        signupButton.setOnClickListener(this);
        loginButton.setOnClickListener(this);
    }

    @Override
    protected void onResume() {
        super.onResume();
        OngoSettings.initialize(this);
        SyncManager.performStartupTasks();
        if (!(getIntent().getBooleanExtra("autologin", false))) {
            performAuthentication();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        callbackManager.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.signup_button:
                Intent signupIntent = new Intent(this, SignupNamesActivity.class);
                startActivity(signupIntent);
                break;
            case R.id.login_button:
                Intent loginIntent = new Intent(this, LoginActivity.class);
                startActivity(loginIntent);
                break;
        }
    }

    /**
     * Shows the progress UI and hides the login form.
     */
    @TargetApi(Build.VERSION_CODES.HONEYCOMB_MR2)
    private void showProgress(final boolean show) {
        // On Honeycomb MR2 we have the ViewPropertyAnimator APIs, which allow
        // for very easy animations. If available, use these APIs to fade-in
        // the progress spinner.
//        int shortAnimTime = getResources().getInteger(android.R.integer.config_longAnimTime);
        progressBar = (ProgressBar) findViewById(R.id.login_progress);
//        final ConstraintLayout loginForm = (ConstraintLayout) findViewById(R.id.supe);
        fbLoginButton.setVisibility(show ? View.GONE : View.VISIBLE);
        loginButton.setVisibility(show ? View.GONE : View.VISIBLE);
        signupButton.setVisibility(show ? View.GONE : View.VISIBLE);
        tagLine.setVisibility(show ? View.GONE : View.VISIBLE);
//        loginForm.animate().setDuration(shortAnimTime).alpha(
//                show ? 0 : 1).setListener(new AnimatorListenerAdapter() {
//            @Override
//            public void onAnimationEnd(Animator animation) {
//                loginForm.setVisibility(show ? View.GONE : View.VISIBLE);
//            }
//        });
        ProgressDialog dialog = ProgressDialog.show(LandingActivity.this, "", "Logging in...", true);
        progressBar.setVisibility(View.VISIBLE);
//        progressBar.animate().alpha(show ? 1 : 0).setListener(new AnimatorListenerAdapter() {
//            @Override
//            public void onAnimationEnd(Animator animation) {
//                progressBar.setVisibility(show ? View.VISIBLE : View.GONE);
//            }
//        });
        progressBar.animate().setDuration(1000).alpha(
                show ? 1 : 0).setListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationEnd(Animator animation) {
                progressBar.setVisibility(show ? View.VISIBLE : View.GONE);
            }
        });
    }

    private void performAuthentication() {
        // Check if credentials are stored
        if (!SecureSettings.isAuthCredentials()) {
            return;
        }
        if (!(getIntent().getBooleanExtra("autologin", false))) {
            return;
        }

        ProgressDialog dialog = ProgressDialog.show(LandingActivity.this, "", "Logging in...", true);

        // Log in if we have stored credentials
        Authentication.getInstance().loginWithStoredCredentials()
                .subscribeOn(Schedulers.newThread())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Observer<AuthResponse>() {
                    @Override
                    public void onSubscribe(Disposable d) {

                    }

                    @Override
                    public void onNext(AuthResponse value) {
                        // Handle login event for Authentication class
                        Authentication.getInstance().handleLogin(value);

                        //track
                        TrackService service = DataSource.getTrackService();
                        // TODO store the API_VERSION somewhere better
                        service.downloadTrack(Authentication.getInstance().getCurrentUser().mainTrack, 4) // api: 4, limit: 10, page: 1
                                .subscribeOn(Schedulers.newThread())
                                .observeOn(AndroidSchedulers.mainThread())
                                .subscribe(new Observer<OGTrack>() {
                                    @Override
                                    public void onSubscribe(Disposable d) {
                                    }

                                    @Override
                                    public void onNext(OGTrack track) {
                                        TrackEnrollmentManager.addOrReplaceTrack(track);
                                        Intent intent = new Intent(LandingActivity.this, TabbedActivity.class);
                                        startActivity(intent);
                                        LandingActivity.this.finish();
                                    }

                                    @Override
                                    public void onError(Throwable e) {
                                        Log.e("Authentication", e.toString());
                                        e.printStackTrace();
                                    }

                                    @Override
                                    public void onComplete() {
                                    }
                                });
                    }

                    @Override
                    public void onError(Throwable e) {
                        //TODO show main landing page
                    }

                    @Override
                    public void onComplete() {

                    }
                });
    }

    private void startSync() {
        EventBus.getDefault().register(this);
        SyncManager.sync();
    }

    @Subscribe
    public void syncStopped(SyncManager.SyncFailedEvent event) {
        onSyncStopped();
    }

    @Subscribe
    public void syncStopped(SyncManager.SyncAbortedEvent event) {
        onSyncStopped();
    }

    @Subscribe
    public void syncStopped(SyncManager.SyncCompletedEvent event) {
        onSyncStopped();
    }

    private void onSyncStopped() {
        EventBus.getDefault().unregister(this);
    }
}
