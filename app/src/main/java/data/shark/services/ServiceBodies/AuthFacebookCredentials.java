package data.shark.services.ServiceBodies;

import com.facebook.AccessToken;
import com.google.gson.annotations.SerializedName;

/**
 * Created by mujtaba on 5/30/17.
 */

public class AuthFacebookCredentials {

    @SerializedName("access_token")
    public String accessToken;

    public AuthFacebookCredentials(AccessToken acToken) {
        accessToken = acToken.getToken();
    }
}
