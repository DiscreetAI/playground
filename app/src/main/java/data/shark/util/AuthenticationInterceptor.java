package data.shark.util;

import java.io.IOException;

import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;

/**
 * Created by mujtaba on 5/25/17.
 * <p>
 * The AuthenticationInterceptor adds the Authorization header to the request if the user has
 * logged in.
 */

public class AuthenticationInterceptor implements Interceptor {

    @Override
    public Response intercept(Chain chain) throws IOException {
        Request request = chain.request();

        // Build new request
        Request.Builder builder = request.newBuilder();
        builder.header("Accept", "application/json");

        // Get the authentication token if the user has logged in
        String token = Authentication.getInstance().getAuthToken();
        if (token != null) {
            builder.header("Authorization", String.format("Bearer %s", token));
        }

        // Do the request and return the response - nothing special here
        request = builder.build();
        Response response = chain.proceed(request);
        return response;
    }

}
