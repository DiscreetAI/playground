package data.shark.services.ServiceBodies;

/**
 * Created by QuickCap on 8/1/2017.
 */

public class PasswordHolder {
    String oldPassword;
    String newPassword;

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    public void setOldPassword(String oldPassword) {
        this.oldPassword = oldPassword;
    }
}
