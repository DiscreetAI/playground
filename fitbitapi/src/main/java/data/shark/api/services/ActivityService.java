package data.shark.api.services;

import data.shark.api.exceptions.MissingScopesException;
import data.shark.api.exceptions.TokenExpiredException;
import data.shark.api.loaders.ResourceLoaderFactory;
import data.shark.api.loaders.ResourceLoaderResult;
import data.shark.api.models.DailyActivitySummary;
import data.shark.authentication.Scope;

import android.app.Activity;
import android.content.Loader;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Created by jboggess on 10/3/16.
 */
public class ActivityService {

    private final static String ACTIVITIES_URL = "https://api.fitbit.com/1/user/-/activities/date/%s.json";
    private static final ResourceLoaderFactory<DailyActivitySummary> USER_ACTIVITIES_LOADER_FACTORY = new ResourceLoaderFactory<>(ACTIVITIES_URL, DailyActivitySummary.class);
    private static final DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.US);

    public static Loader<ResourceLoaderResult<DailyActivitySummary>> getDailyActivitySummaryLoader(Activity activityContext, Date date) throws MissingScopesException, TokenExpiredException {
        return USER_ACTIVITIES_LOADER_FACTORY.newResourceLoader(activityContext, new Scope[]{Scope.activity}, dateFormat.format(date));
    }

}
