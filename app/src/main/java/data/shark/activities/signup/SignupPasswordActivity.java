package data.shark.activities.signup;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.design.widget.TextInputLayout;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.CardView;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import data.shark.activities.tab.TabbedActivity;
import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import data.shark.R;
import data.shark.services.ServiceBodies.AuthResponse;
import data.shark.services.ServiceBodies.AuthSignupParameters;
import data.shark.util.Authentication;
import data.shark.util.FontUtilities;

public class SignupPasswordActivity extends AppCompatActivity implements View.OnClickListener {

    private EditText passwordEntry;
    private CardView nextButton;

    private String emptyErrorMsg;
    private String invalidErrorMsg;
    private Drawable errorIcon;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup_password);

        //UI Components
        TextView questionText = (TextView) findViewById(R.id.title);
        TextInputLayout passwordLayout = (TextInputLayout) findViewById(R.id.passwordInputLayout);
        passwordEntry = (EditText) findViewById(R.id.editPassword);
        TextView passwordReq = (TextView) findViewById(R.id.passwordRequirement);
        nextButton = (CardView) findViewById(R.id.nextButton);
        TextView buttonText = (TextView) findViewById(R.id.buttonText);

        //Set fonts
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] medTextViews = new TextView[]{questionText, buttonText};
        TextView[] regTextViews = new TextView[]{passwordEntry, passwordReq};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);
        FontUtilities.setFonts(passwordLayout, fontUtilities.scandiaRegular);

        //Set error message and icon
        emptyErrorMsg = getString(R.string.error_field_required);
        invalidErrorMsg = getString(R.string.error_invalid_password);
        errorIcon = getDrawable(R.drawable.ic_error);
        if (errorIcon != null) {
            errorIcon.setBounds(0, 0, errorIcon.getIntrinsicWidth(), errorIcon.getIntrinsicHeight());
        }

        addTextWatcher(passwordEntry);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.nextButton:
                signUp();
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
        nextButton.setBackgroundColor(ContextCompat.getColor(this, R.color.white));
        nextButton.setOnClickListener(this);
    }

    /**
     * Doesn't allow user to click next button
     */
    private void disableNextButton() {
        nextButton.setBackgroundColor(ContextCompat.getColor(this, R.color.paleRed));
        nextButton.setOnClickListener(v -> {
            if (isEmpty(passwordEntry.getText())) {
                passwordEntry.setError(emptyErrorMsg, errorIcon);
            } else {
                passwordEntry.setError(invalidErrorMsg, errorIcon);
            }
        });
    }

    /**
     * Sign up user using name, email, and password entered
     */
    private void signUp() {
        String password = passwordEntry.getText().toString();
        Intent prevIntent = getIntent();

        //Get entered information as parameters for signup
        AuthSignupParameters params = new AuthSignupParameters(
                prevIntent.getStringExtra("first name"), prevIntent.getStringExtra("last name"),
                prevIntent.getStringExtra("email"), password);

        //Sign up using parameters
        Authentication.getInstance().signupWithParameters(params)
                .subscribeOn(Schedulers.newThread())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Observer<AuthResponse>() {
                    @Override
                    public void onSubscribe(Disposable d) {
                    }

                    @Override
                    public void onNext(AuthResponse value) {
                        //Launch activity
                        Authentication.getInstance().setCurrentUser(value.user);
                        Authentication.getInstance().setAuthToken(value.token);
                        Intent informationIntent = new Intent(getApplicationContext(),
                                TabbedActivity.class);
                        startActivity(informationIntent);
                    }

                    @Override
                    public void onError(Throwable e) {
                        Log.e("SignupPasswordActivity", e.toString());
                    }

                    @Override
                    public void onComplete() {
                    }
                });
    }
}
