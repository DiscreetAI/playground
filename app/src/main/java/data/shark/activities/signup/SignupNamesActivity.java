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

import data.shark.R;
import data.shark.util.FontUtilities;

public class SignupNamesActivity extends AppCompatActivity implements View.OnClickListener {

    private EditText firstNameEntry;
    private EditText lastNameEntry;
    private CardView nextButton;

    private String errorMsg;
    private Drawable errorIcon;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup_names);

        //UI Components
        TextView questionText = (TextView) findViewById(R.id.title);
        TextInputLayout firstNameLayout = (TextInputLayout) findViewById(R.id.firstNameInputLayout);
        firstNameEntry = (EditText) findViewById(R.id.editFirstName);
        TextInputLayout lastNameLayout = (TextInputLayout) findViewById(R.id.lastNameInputLayout);
        lastNameEntry = (EditText) findViewById(R.id.editLastName);
        nextButton = (CardView) findViewById(R.id.nextButton);
        TextView buttonText = (TextView) findViewById(R.id.buttonText);

        //Set fonts
        FontUtilities fontUtilities = new FontUtilities(this);
        TextView[] medTextViews = new TextView[]{questionText, buttonText};
        TextView[] regTextViews = new TextView[]{firstNameEntry, lastNameEntry};
        TextInputLayout[] regTextLayouts = new TextInputLayout[]{firstNameLayout, lastNameLayout};
        FontUtilities.setFonts(medTextViews, fontUtilities.scandiaMedium);
        FontUtilities.setFonts(regTextViews, fontUtilities.scandiaRegular);
        FontUtilities.setFonts(regTextLayouts, fontUtilities.scandiaRegular);

        //Set error message and icon
        errorMsg = getString(R.string.error_field_required);
        errorIcon = getDrawable(R.drawable.ic_error);
        if (errorIcon != null) {
            errorIcon.setBounds(0, 0, errorIcon.getIntrinsicWidth(), errorIcon.getIntrinsicHeight());
        }

        addTextWatcher(firstNameEntry, lastNameEntry);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.nextButton:
                String firstNameText = firstNameEntry.getText().toString();
                String lastNameText = lastNameEntry.getText().toString();
                Intent intent = new Intent(this, SignupEmailActivity.class);
                intent.putExtra("first name", firstNameText);
                intent.putExtra("last name", lastNameText);
                startActivity(intent);
                break;
            default:
                break;
        }
    }

    /**
     * Check if name is valid
     */
    private boolean isValidName(CharSequence name) {
        return name.length() > 0;
    }

    /**
     * Adds check mark to end of EditTexts when the fields satisfy requirements
     * and error icon when the fields don't satisfy requirements.
     */
    private void addTextWatcher(final EditText editText1, final EditText editText2) {
        disableNextButton();

        //Listens for changes to text in first field
        editText1.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                //Check if field is not empty
                if (isValidName(s)) {
                    //Display check mark
                    editText1.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.ic_check_white, 0);
                    //Check if other field is also not empty
                    if (isValidName(editText2.getText())) {
                        enableNextButton();
                    }
                } else {
                    //Display error and disable button
                    editText1.setError(errorMsg, errorIcon);
                    disableNextButton();
                }
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        //Listens for changes to text in second field
        editText2.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                //Check if field is not empty
                if (isValidName(s)) {
                    //Display check mark
                    editText2.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.ic_check_white, 0);
                    //Check if other field is also not empty
                    if (isValidName(editText1.getText())) {
                        enableNextButton();
                    }
                } else {
                    //Display error and disable button
                    editText2.setError(errorMsg, errorIcon);
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
            if (!isValidName(firstNameEntry.getText())) {
                firstNameEntry.setError(errorMsg, errorIcon);
            }
            if (!isValidName(lastNameEntry.getText())) {
                lastNameEntry.setError(errorMsg, errorIcon);
            }
        });
    }
}
