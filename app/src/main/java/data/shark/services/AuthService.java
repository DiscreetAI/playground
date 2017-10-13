package data.shark.services;

import io.reactivex.Observable;
import data.shark.services.ServiceBodies.AuthCredentials;
import data.shark.services.ServiceBodies.AuthFacebookCredentials;
import data.shark.services.ServiceBodies.AuthResponse;
import data.shark.services.ServiceBodies.AuthSignupParameters;
import retrofit2.http.Body;
import retrofit2.http.POST;

/**
 * Created by mujtaba on 5/25/17.
 */

public interface AuthService {

    @POST("auth/local/login")
    Observable<AuthResponse> loginWithCredentials(@Body AuthCredentials credentials);

    @POST("auth/facebook/login")
    Observable<AuthResponse> loginWithFacebook(@Body AuthFacebookCredentials credentials);

    @POST("api/users/signup")
    Observable<AuthResponse> signupUser(@Body AuthSignupParameters parameters);
}
