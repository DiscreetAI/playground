package data.shark.api.services;

import data.shark.api.exceptions.MissingScopesException;
import data.shark.api.exceptions.TokenExpiredException;
import data.shark.api.loaders.ResourceLoaderFactory;
import data.shark.api.loaders.ResourceLoaderResult;
import data.shark.api.models.Device;
import data.shark.authentication.Scope;

import android.app.Activity;
import android.content.Loader;

/**
 * Created by jboggess on 9/14/16.
 */
public class DeviceService {

    private final static String DEVICE_URL = "https://api.fitbit.com/1/user/-/devices.json";
    private static final ResourceLoaderFactory<Device[]> USER_DEVICES_LOADER_FACTORY = new ResourceLoaderFactory<>(DEVICE_URL, Device[].class);

    public static Loader<ResourceLoaderResult<Device[]>> getUserDevicesLoader(Activity activityContext) throws MissingScopesException, TokenExpiredException {
        return USER_DEVICES_LOADER_FACTORY.newResourceLoader(activityContext, new Scope[]{Scope.settings});
    }

}
