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
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import data.shark.R;
import data.shark.util.FontUtilities;

public class SignupEmailActivity extends AppCompatActivity implements View.OnClickListener {

    private static final Pattern VALID_EMAIL_ADDRESS_REGEX =
            Pattern.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}$", Pattern.CASE_INSENSITIVE);

    private EditText emailEntry;
    private CardView nextButton;

    private String emptyErrorMsg;
    private String invalidErrorMsg;
    private Drawable errorIcon;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup_email);

        //UI Components
        TextView questionText = (TextView) findViewById(R.id.title);
        TextInputLayout emailLayout = (TextInputLayout) findViewById(R.id.emailInputLayout);
        emailEntry = (EditText) findViewById(R.id.editEmail);
        nextButton = (CardView) findViewById(R.id.nextButton);
        TextView buttonText = (TextView) findViewById(R.id.buttonText);

        //Add user's name to greeting
        Intent prevIntent = getIntent();
        String firstName = prevIntent.getStringExtra("first name");
        String greeting = "Hi " + firstName + "! Let's get you set up.";
        questionText.setText(greeting);

        //Set fonts
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] medTextViews = new TextView[]{questionText, buttonText};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        FontUtilities.setFonts(emailEntry, fontUtilities.scandiaRegular);
        FontUtilities.setFonts(emailLayout, fontUtilities.scandiaRegular);

        //Set error message and icon
        emptyErrorMsg = getString(R.string.error_field_required);
        invalidErrorMsg = getString(R.string.error_invalid_email);
        errorIcon = getDrawable(R.drawable.ic_error);
        if (errorIcon != null) {
            errorIcon.setBounds(0, 0, errorIcon.getIntrinsicWidth(), errorIcon.getIntrinsicHeight());
        }

        addTextWatcher(emailEntry);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.nextButton:
                String email = emailEntry.getText().toString();
                Intent intent = new Intent(this, SignupPasswordActivity.class);
                intent.putExtra("first name", getIntent().getStringExtra("first name"));
                intent.putExtra("last name", getIntent().getStringExtra("last name"));
                intent.putExtra("email", email);
                startActivity(intent);
                break;
            default:
                break;
        }
    }

    /**
     * Check if email is valid
     */
    private boolean isValidEmail(CharSequence email) {
        Matcher matcher = VALID_EMAIL_ADDRESS_REGEX.matcher(email);
        return matcher.find();
    }

    /**
     * Check if email field is empty
     */
    private boolean isEmpty(CharSequence email) {
        return email.length() == 0;
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
                if (!isEmpty(s) && isValidEmail(s)) {
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
            if (isEmpty(emailEntry.getText())) {
                emailEntry.setError(emptyErrorMsg, errorIcon);
            } else {
                emailEntry.setError(invalidErrorMsg, errorIcon);
            }
        });
    }
}
