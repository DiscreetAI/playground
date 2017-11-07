package data.shark.activities.tab;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;

import data.shark.authentication.AuthenticationHandler;
import data.shark.authentication.AuthenticationManager;

import data.shark.R;
import data.shark.authentication.AuthenticationResult;
import data.shark.sampleandroidoauth2.FitbitAuthApplication;

public class TabbedActivity extends AppCompatActivity implements AuthenticationHandler{


    private ViewPager viewPager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tabbed);
        FitbitAuthApplication app = new FitbitAuthApplication();
        //Three Tab Layout
        TabPagerAdapter adapter = new TabPagerAdapter(getSupportFragmentManager(), 3);
        viewPager = (ViewPager) findViewById(R.id.pager);
        viewPager.setAdapter(adapter);
        viewPager.setOffscreenPageLimit(2);

        TabLayout tabLayout = (TabLayout) findViewById(R.id.tabs);
        tabLayout.setupWithViewPager(viewPager);
        tabLayout.getTabAt(0).setIcon(R.drawable.ic_tab_activity);
        tabLayout.getTabAt(1).setIcon(R.drawable.ic_tab_home).select();
        tabLayout.getTabAt(2).setIcon(R.drawable.ic_tab_settings);
        tabLayout.setTabGravity(TabLayout.GRAVITY_FILL);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Fragment fragment = getSupportFragmentManager().findFragmentById(R.id.homeFragment);
        AuthenticationHandler authenticationHandler = (AuthenticationHandler) fragment;
        AuthenticationManager.onActivityResult(requestCode, resultCode, data, this);
//        callbackManager.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    public void onAuthFinished(AuthenticationResult result) {
        System.out.println("I did it!");
    }
}
