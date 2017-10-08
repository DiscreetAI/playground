package data.shark.activities.tab;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

import data.shark.activities.tab.settings.SettingsFragment;

/**
 * Instantiates and organizes fragments for the five tabs in TabbedActivity
 */
public class TabPagerAdapter extends FragmentPagerAdapter {
    private int numTabs;

    TabPagerAdapter(FragmentManager fm, int num) {
        super(fm);
        this.numTabs = num;
    }

    @Override
    public Fragment getItem(int position) {
        switch (position) {
            case 0:
                return GraphFragment.newInstance(0);
            case 1:
                return HomeFragment.newInstance(1);
            case 2:
                return SettingsFragment.newInstance(2);
            default:
                return null;
        }
    }

    @Override
    public int getItemPosition(Object item) {
        Fragment mFragment = (Fragment) item;
        int i = mFragment.getArguments().getInt("index");
        switch (i) {
            case 2:
                return POSITION_NONE;
            case 0:
                return POSITION_NONE;
            default:
                return i;
        }
    }

    @Override
    public int getCount() {
        return numTabs;
    }
}
