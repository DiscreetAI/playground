package data.shark.services.ServiceBodies;

/**
 * Created by mujtaba on 5/30/17.
 */

public class AuthSignupParameters {

    public String firstName;
    public String lastName;
    public String email;
    public String password;

    public AuthSignupParameters(String f, String l, String e, String p) {
        firstName = f;
        lastName = l;
        email = e;
        password = p;
    }
}
