package data.shark.activities.profile;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import de.hdodenhof.circleimageview.CircleImageView;
import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import data.shark.R;
import data.shark.models.OGUser;
import data.shark.services.ServiceBodies.UserProfile;
import data.shark.util.Authentication;
import data.shark.util.FontUtilities;

/**
 * Edit current user's profile information including
 * profile picture, name, location, gender, birthday, and weight
 */

public class EditProfileActivity extends AppCompatActivity implements View.OnClickListener {

    private static final int EDIT_REQUEST = 2;
    private static final SimpleDateFormat SDF = new SimpleDateFormat("MMM dd, yyyy", Locale.US);
    private static FragmentManager fragmentManager;
    private CircleImageView profPic;
    private TextView emailEntry;
    private EditText firstNameEntry;
    private EditText lastNameEntry;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_profile);

        //Toolbar
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        fragmentManager = getSupportFragmentManager();

        //UI components
        TextView title = (TextView) findViewById(R.id.title);
        ImageView backArrow = (ImageView) findViewById(R.id.back_arrow);
        TextView saveButton = (TextView) findViewById(R.id.save_button);
        TextView profPicHeader = (TextView) findViewById(R.id.profPicHeader);
        profPic = (CircleImageView) findViewById(R.id.profile_pic);
        TextView emailHeader = (TextView) findViewById(R.id.emailHeader);
        emailEntry = (TextView) findViewById(R.id.emailEntry);
        TextView firstNameHeader = (TextView) findViewById(R.id.firstNameHeader);
        firstNameEntry = (EditText) findViewById(R.id.firstNameEntry);
        TextView lastNameHeader = (TextView) findViewById(R.id.lastNameHeader);
        lastNameEntry = (EditText) findViewById(R.id.lastNameEntry);

        //Set fonts
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] medTextViews = new TextView[]{title, saveButton};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        TextView[] regTextViews = new TextView[]{profPicHeader, emailHeader, emailEntry,
                firstNameHeader, firstNameEntry, lastNameHeader, lastNameEntry};
        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);

        setUserInfo(Authentication.getInstance().getCurrentUser());

        backArrow.setOnClickListener(this);
        saveButton.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.back_arrow:
                finish();
                break;
            case R.id.save_button:
                saveUserInfo();
                break;
            default:
                break;
        }
    }

    /**
     * Read user info from backend and set text in UI
     */
    private void setUserInfo(OGUser currUser) {
        Picasso.with(getApplicationContext()).load(currUser.avatarUrl).into(profPic);
        emailEntry.setText(currUser.email);
        firstNameEntry.setText(currUser.firstName);
        lastNameEntry.setText(currUser.lastName);
    }

    /**
     * Update user profile in backend
     */
    private void saveUserInfo() {
        UserProfile userProfile = new UserProfile();
        userProfile.firstName = firstNameEntry.getText().toString();
        userProfile.lastName = lastNameEntry.getText().toString();
        Authentication.getInstance().updateProfile(Authentication.getInstance().getCurrentUserId(),
                userProfile)
                .subscribeOn(Schedulers.newThread())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Observer<OGUser>() {
                    @Override
                    public void onSubscribe(Disposable d) {

                    }

                    @Override
                    public void onNext(OGUser value) {
                        Authentication.getInstance().setCurrentUser(value);
                        Intent saveIntent = new Intent(getApplicationContext(), ProfileActivity.class);
                        startActivity(saveIntent);
                    }

                    @Override
                    public void onError(Throwable e) {
                        Log.e("error", e.toString());
                    }

                    @Override
                    public void onComplete() {

                    }
                });
    }
}
