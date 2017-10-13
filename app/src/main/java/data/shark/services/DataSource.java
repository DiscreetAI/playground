package data.shark.services;

import data.shark.util.Authentication;

/**
 * Created by mujtaba on 6/8/17.
 */

public class DataSource {

    public static AuthService getAuthService() {
        return Authentication.authService();
    }


    public static UserService getUserService() {
        return Authentication.retrofit().create(UserService.class);
    }

}
