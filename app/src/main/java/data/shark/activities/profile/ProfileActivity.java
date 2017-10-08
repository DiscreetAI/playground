package data.shark.activities.profile;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.facebook.AccessToken;
import com.facebook.GraphRequest;
import com.squareup.picasso.Picasso;

import java.util.Locale;

import de.hdodenhof.circleimageview.CircleImageView;
import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import data.shark.R;
import data.shark.models.OGUser;
import data.shark.services.DataSource;
import data.shark.services.ServiceBodies.FollowResponse;
import data.shark.services.ServiceBodies.FriendRequest;
import data.shark.services.UserService;
import data.shark.util.Authentication;
import data.shark.util.FontUtilities;
import retrofit2.Response;

/**
 * Display user profile information and current programs
 */
public class ProfileActivity extends AppCompatActivity implements View.OnClickListener {

    private TextView userNameText;
    private CircleImageView profilePic;
    private String uId;
    private boolean main;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        //UI elements
        uId = getIntent().getStringExtra("userId");
        if (uId == null) {
            main = true;
        }
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        userNameText = (TextView) findViewById(R.id.name);
        TextView editButton = (TextView) findViewById(R.id.edit_button);
        profilePic = (CircleImageView) findViewById(R.id.profile_pic);
        ImageView backArrow = (ImageView) findViewById(R.id.back_arrow);

//        setUserInfoFB();

        editButton.setOnClickListener(this);
        backArrow.setOnClickListener(this);

        //Set fonts of TextViews
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] medTextViews = new TextView[]{userNameText, editButton};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        setUserInfo();
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.back_arrow:
                finish();
                break;
            case R.id.edit_button:
                Intent editIntent = new Intent(this, EditProfileActivity.class);
                startActivity(editIntent);
                break;
            default:
                break;
        }
    }

    /**
     * Read user info from Realm DB and set text in UI
     */
    private void setUserInfo() {
            OGUser currUser = Authentication.getInstance().getCurrentUser();
            userNameText.setText(currUser.fullName());
    }

    private void setUserInfoFB() {
        GraphRequest request = GraphRequest.newMeRequest(
                AccessToken.getCurrentAccessToken(),
                (object, response) -> {
                    // Application code
                });
        Bundle parameters = new Bundle();
        parameters.putString("fields", "id,name,link");
        request.setParameters(parameters);
        request.executeAsync();
    }

}
