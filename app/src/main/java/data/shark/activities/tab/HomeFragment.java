package data.shark.activities.tab;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.constraint.ConstraintLayout;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.LinearSnapHelper;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.SnapHelper;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.nshmura.snappysmoothscroller.SnappyLinearLayoutManager;
import com.squareup.picasso.Picasso;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import data.shark.R;
import data.shark.activities.profile.ProfileActivity;
import data.shark.models.OGUser;
import data.shark.services.DataSource;
import data.shark.util.Authentication;
import data.shark.util.FontUtilities;

/**
 * Second tab in TabbedActivity
 * Greets user and displays progress in their current program
 */
public class HomeFragment extends Fragment implements View.OnClickListener {

    private Context context;
    private TextView money;

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
        TextView money = (TextView) view.findViewById(R.id.money);

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
                Intent profileIntent = new Intent(context, ProfileActivity.class);
                startActivity(profileIntent);
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
