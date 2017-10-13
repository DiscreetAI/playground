package data.shark.activities.tab;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.TabLayout;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;

import com.facebook.CallbackManager;

import data.shark.R;

public class TabbedActivity extends AppCompatActivity {

    CallbackManager callbackManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tabbed);

        //Three Tab Layout
        TabPagerAdapter adapter = new TabPagerAdapter(getSupportFragmentManager(), 3);
        ViewPager viewPager = (ViewPager) findViewById(R.id.pager);
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
        callbackManager.onActivityResult(requestCode, resultCode, data);
    }
}
