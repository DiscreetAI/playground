package data.shark.api.services;

import data.shark.api.exceptions.MissingScopesException;
import data.shark.api.exceptions.TokenExpiredException;
import data.shark.api.loaders.ResourceLoaderFactory;
import data.shark.api.loaders.ResourceLoaderResult;
import data.shark.api.models.UserContainer;
import com.fitbit.authentication.Scope;

import android.app.Activity;
import android.content.Loader;

/**
 * Created by jboggess on 9/14/16.
 */
public class UserService {

    private final static String USER_URL = "https://api.fitbit.com/1/user/-/profile.json";
    private static final ResourceLoaderFactory<UserContainer> USER_PROFILE_LOADER_FACTORY = new ResourceLoaderFactory<>(USER_URL, UserContainer.class);

    public static Loader<ResourceLoaderResult<UserContainer>> getLoggedInUserLoader(Activity activityContext) throws MissingScopesException, TokenExpiredException {
        return USER_PROFILE_LOADER_FACTORY.newResourceLoader(activityContext, new Scope[]{Scope.profile});
    }

}
