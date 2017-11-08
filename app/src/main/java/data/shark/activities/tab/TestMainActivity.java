package data.shark.activities.tab;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import data.shark.R;
import data.shark.authentication.AccessToken;
import data.shark.authentication.AuthenticationHandler;
import data.shark.authentication.AuthenticationManager;
import data.shark.authentication.AuthenticationResult;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class TestMainActivity extends AppCompatActivity implements View.OnClickListener, AuthenticationHandler {
    Context context;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test_main);
        money = (TextView) findViewById(R.id.money);
        Button auth = (Button) findViewById(R.id.authorize);
        money.setOnClickListener(this);
        auth.setOnClickListener(this);
        context = getApplicationContext();
    }
    private final String SERVER_BASE_URL = "http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/";
//    private final String SERVER_BASE_URL = "http://localhost:5000/";
    private TextView money;
    public void onLoginClick(View view) {
        AuthenticationManager.login(this);
    }
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        AuthenticationManager.onActivityResult(requestCode, resultCode, data, this);
    }


    @RequiresApi(api = Build.VERSION_CODES.CUPCAKE)
    public void onAuthFinished(AuthenticationResult authenticationResult) {
        if (authenticationResult.isSuccessful()) {
            new PostMethodDemo().execute(SERVER_BASE_URL+"insert", authenticationResult.getAccessToken() );
            money.setText("you are on your way to making money!");
        } else {
            money.setText("you are a failure");
            //Uh oh... errors...
        }
    }
    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.money:
                money.setText("Make some money!");
                break;
            case R.id.authorize:
                AuthenticationManager.login(this);
                break;
            default:
                break;
        }
    }
    private class PostMethodDemo {
        RequestQueue MyRequestQueue = Volley.newRequestQueue(context);

        public void execute(String s, AccessToken accessToken) {
            Log.v("accessToken", accessToken.getAccessToken());
            //Create an error listener to handle errors appropriately.
            StringRequest MyStringRequest = new StringRequest(Request.Method.POST, s, response -> {
                //This code is executed if the server responds, whether or not the response contains data.
                //The String 'response' contains the server's response.
                Log.e("responded!", response);
            }, error -> {
                //This code is executed if there is an error.
                Log.e("sadbois","there was an error");
            }) {
                protected Map<String, String> getParams() {
                    Map<String, String> MyData = new HashMap<>();
                    MyData.put("accessToken", accessToken.getAccessToken());
                    //Add the data you'd like to send to the server.
                    return MyData;
                }
            };
            MyRequestQueue.add(MyStringRequest);
        }
    }
}