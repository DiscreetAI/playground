package data.shark.activities.tab.settings;

import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.design.widget.TextInputLayout;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.CardView;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import data.shark.R;
import data.shark.models.OGUser;
import data.shark.services.DataSource;
import data.shark.services.ServiceBodies.PasswordHolder;
import data.shark.services.UserService;
import data.shark.util.FontUtilities;

public class ChangePasswordActivity extends AppCompatActivity implements View.OnClickListener {

    private EditText currentPasswordEntry;
    private EditText newPasswordEntry;
    private CardView nextButton;

    private String emptyErrorMsg;
    private String invalidErrorMsg;
    private Drawable errorIcon;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password);

        //UI Components
        TextView title = (TextView) findViewById(R.id.title);
        TextInputLayout currentPasswordLayout = (TextInputLayout) findViewById(R.id.currentPasswordInputLayout);
        currentPasswordEntry = (EditText) findViewById(R.id.editCurrentPassword);
        TextInputLayout newPasswordLayout = (TextInputLayout) findViewById(R.id.newPasswordInputLayout);
        newPasswordEntry = (EditText) findViewById(R.id.editNewPassword);
        TextView passwordReq = (TextView) findViewById(R.id.passwordRequirement);
        nextButton = (CardView) findViewById(R.id.nextButton);
        TextView buttonText = (TextView) findViewById(R.id.buttonText);

        //Set fonts
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] medTextViews = new TextView[]{title, buttonText};
        TextView[] regTextViews = new TextView[]{currentPasswordEntry, newPasswordEntry, passwordReq};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);
        TextInputLayout[] regInputLayouts = new TextInputLayout[]{currentPasswordLayout, newPasswordLayout};
        FontUtilities.setFonts(regInputLayouts, fontUtilities.scandiaRegular);

        //Set error message and icon
        emptyErrorMsg = getString(R.string.error_field_required);
        invalidErrorMsg = getString(R.string.error_invalid_password);
        errorIcon = getDrawable(R.drawable.ic_error);
        if (errorIcon != null) {
            errorIcon.setBounds(0, 0, errorIcon.getIntrinsicWidth(), errorIcon.getIntrinsicHeight());
        }
        addTextWatcher(currentPasswordEntry);
        addTextWatcher(newPasswordEntry);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.nextButton:
                changePassword();
                break;
        }
    }

    /**
     * Check if password is valid
     */
    private boolean isValidPassword(CharSequence password) {
        return password.length() >= 8;
    }

    /**
     * Check if password field is empty
     */
    private boolean isEmpty(CharSequence password) {
        return password.length() == 0;
    }

    /**
     * Adds check mark to end of EditText when the field satisfies requirement
     * and error icon when the field doesn't satisfy requirement.
     */
    private void addTextWatcher(final EditText editText) {
        disableNextButton();

        //Listens for changes to text
        editText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                editText.setError(null);
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                //Check if field is not empty and entry is valid
                if (!isEmpty(s) && isValidPassword(s)) {
                    //Display check mark and enable button
                    editText.setCompoundDrawablesWithIntrinsicBounds(0, 0, 0, 0);
                    editText.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.ic_check_white, 0);
                    enableNextButton();
                } else {
                    //Disable button
                    editText.setCompoundDrawablesWithIntrinsicBounds(0, 0, 0, 0);
                    editText.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.ic_error, 0);
                    disableNextButton();
                }
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });
    }

    /**
     * Allow user to click next button
     */
    private void enableNextButton() {
        nextButton.setOnClickListener(this);
    }

    /**
     * Doesn't allow user to click next button
     */
    private void disableNextButton() {
        nextButton.setOnClickListener(v -> {
            if (isEmpty(currentPasswordEntry.getText())) {
                currentPasswordEntry.setError(emptyErrorMsg, errorIcon);
            } else {
                currentPasswordEntry.setError(invalidErrorMsg, errorIcon);
            }
            if (isEmpty(newPasswordEntry.getText())) {
                newPasswordEntry.setError(emptyErrorMsg, errorIcon);
            } else {
                newPasswordEntry.setError(invalidErrorMsg, errorIcon);
            }
        });
    }

    /**
     * Changes user's password
     */
    private void changePassword() {
        String currentPassword = currentPasswordEntry.getText().toString();
        String newPassword = newPasswordEntry.getText().toString();
        PasswordHolder passwordHolder = new PasswordHolder();
        passwordHolder.setNewPassword(newPassword);
        passwordHolder.setOldPassword(currentPassword);
        UserService service = DataSource.getUserService();
        service.resetPassword(passwordHolder)
                .subscribeOn(Schedulers.newThread())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Observer<OGUser>() {
                    @Override
                    public void onSubscribe(Disposable d) {

                    }

                    @Override
                    public void onNext(OGUser value) {
                        Log.e("password", "successfullychanged");
                    }

                    @Override
                    public void onError(Throwable e) {
                        Log.e("passworderror", e.toString());
                    }

                    @Override
                    public void onComplete() {

                    }
                });
    }
}
