package data.shark.activities.tab.settings;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.constraint.ConstraintLayout;
import android.support.v4.app.Fragment;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import de.hdodenhof.circleimageview.CircleImageView;
import data.shark.R;
import data.shark.activities.profile.ProfileActivity;
import data.shark.models.OGUser;
import data.shark.util.Authentication;
import data.shark.util.FontUtilities;

/**
 * Fifth tab in TabbedActivity
 * Settings and information regarding account, legal, and software
 */
public class SettingsFragment extends Fragment implements View.OnClickListener {
    Context context;
    CircleImageView profilePic;
    TextView name;
    TextView email;

    public static SettingsFragment newInstance(int index) {
        SettingsFragment fragment = new SettingsFragment();
        Bundle args = new Bundle();
        args.putInt("index", index);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_settings, container, false);
        context = getContext();

        //Toolbar
        Toolbar toolbar = (Toolbar) view.findViewById(R.id.toolbar);
        ((AppCompatActivity) getActivity()).setSupportActionBar(toolbar);
        TextView title = (TextView) view.findViewById(R.id.title);

        //Profile
        ConstraintLayout profileButton = (ConstraintLayout) view.findViewById(R.id.profileButton);
        profilePic = (CircleImageView) view.findViewById(R.id.profile_pic);
        name = (TextView) view.findViewById(R.id.name);
        email = (TextView) view.findViewById(R.id.email);

        //Account Settings
        TextView accountHeader = (TextView) view.findViewById(R.id.accountHeader);
        Button notifications = (Button) view.findViewById(R.id.notifications);
        Button changePassword = (Button) view.findViewById(R.id.changePassword);
        Button restorePurchases = (Button) view.findViewById(R.id.restorePurchases);
        Button logout = (Button) view.findViewById(R.id.logout);

        //Legal Settings
        TextView legalHeader = (TextView) view.findViewById(R.id.legalHeader);
        Button terms = (Button) view.findViewById(R.id.terms);
        Button privacyPolicy = (Button) view.findViewById(R.id.privacyPolicy);

        //Software Settings
        TextView softwareHeader = (TextView) view.findViewById(R.id.softwareHeader);
        Button version = (Button) view.findViewById(R.id.version);
        Button clearCache = (Button) view.findViewById(R.id.clearCache);

        //Set fonts of TextViews
        FontUtilities fontUtilities = new FontUtilities(context);
        TextView[] medTextViews = new TextView[]{title, name};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        TextView[] regTextViews = new TextView[]{email, accountHeader, notifications,
                changePassword, restorePurchases, logout, legalHeader, terms, privacyPolicy,
                softwareHeader, version, clearCache};
        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);

        profileButton.setOnClickListener(this);
        notifications.setOnClickListener(this);
        changePassword.setOnClickListener(this);
        restorePurchases.setOnClickListener(this);
        logout.setOnClickListener(this);
        terms.setOnClickListener(this);
        privacyPolicy.setOnClickListener(this);
        version.setOnClickListener(this);
        clearCache.setOnClickListener(this);
        setUserInfo();
        return view;
    }

    private void setUserInfo() {
        try {
            OGUser currUser = Authentication.getInstance().getCurrentUser();
            name.setText(currUser.fullName());
            email.setText(currUser.email);
            Picasso.with(getContext()).load(currUser.avatarUrl).into(profilePic);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.profileButton:
                Intent profileIntent = new Intent(context, ProfileActivity.class);
                startActivity(profileIntent);
                break;
            case R.id.changePassword:
                Intent changePwIntent = new Intent(context, ChangePasswordActivity.class);
                startActivity(changePwIntent);
                break;
            case R.id.restorePurchases:
                //TODO: Restore purchases onClick
                break;
            case R.id.logout:
                Authentication auth = Authentication.getInstance();
                auth.logout(getActivity());
                break;
            case R.id.terms:
                Intent termsIntent = new Intent(Intent.ACTION_VIEW,
                        Uri.parse("https://app.ongo.life/tos"));
                startActivity(termsIntent);
                break;
            case R.id.privacyPolicy:
                Intent privacyIntent = new Intent(Intent.ACTION_VIEW,
                        Uri.parse("https://app.ongo.life/privacy"));
                startActivity(privacyIntent);
                break;
            case R.id.version:
                //TODO: Version settings onClick
                break;
            case R.id.clearCache:
                //TODO: Clear cache onClick
                break;
            default:
                break;
        }
    }
}
