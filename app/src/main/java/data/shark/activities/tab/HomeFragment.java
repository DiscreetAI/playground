package data.shark.activities.tab;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import data.shark.R;
import data.shark.authentication.AuthenticationHandler;
import data.shark.authentication.AuthenticationManager;
import data.shark.authentication.AuthenticationResult;

/**
 * Second tab in TabbedActivity
 * Greets user and displays progress in their current program
 */
public class HomeFragment extends Fragment implements View.OnClickListener, AuthenticationHandler {
    private final String SERVER_BASE_URL = "http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/";
    private Context context;
    private TextView money;
    public void onLoginClick(View view) {
        AuthenticationManager.login(this.getActivity());
    }
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        AuthenticationManager.onActivityResult(requestCode, resultCode, data, this);
    }


    @RequiresApi(api = Build.VERSION_CODES.CUPCAKE)
    public void onAuthFinished(AuthenticationResult authenticationResult) {
        if (authenticationResult.isSuccessful()) {
//            new GetMethodDemo().execute(SERVER_BASE_URL+"/insert");
            money.setText("you are on your way to making money!");
        } else {
            money.setText("you are a failure");
            //Uh oh... errors...
        }
    }
    public static HomeFragment newInstance(int index) {
        HomeFragment fragment = new HomeFragment();
        Bundle args = new Bundle();
        args.putInt("index", index);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        context = getContext();
        money = (TextView) view.findViewById(R.id.money);
        Button auth = (Button) view.findViewById(R.id.authorize);
        money.setOnClickListener(this);
        auth.setOnClickListener(this);
        //Set fonts of TextViews
//        FontUtilities fontUtilities = new FontUtilities(getContext());
//        TextView[] medTextViews = new TextView[]{title, userName, sessionName, buttonText,
//                activityName, progressHeader};
//        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
//        TextView[] regTextViews = new TextView[]{recentActivityHeader, genre, programName,
//                numSessions, numSessionsText, startDate, startText, finishDate, finishText,
//                newSessionText, oneSessionText};
//        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);
        return view;
    }

    /**
     * Changes the greeting and background art on screen based on the time of day
     */



    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.money:
                money.setText("Make some money!");
                break;
            case R.id.authorize:
                AuthenticationManager.login(this.getActivity());
                break;
//            case R.id.card:
//                Intent activityIntent = new Intent(context, SessionDetailActivity.class);
//                activityIntent.putExtra("trackId", trackId);
//                activityIntent.putExtra("sessionId", sessionId);
//                startActivity(activityIntent);
//                break;
//            case R.id.activityButton:
//                Intent activeIntent = new Intent(context, ActivityRecentActivity.class);
//                startActivity(activeIntent);
//                break;
            default:
                break;
        }
    }
}
