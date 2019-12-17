package com.example.shakti.advsf;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.widget.TextView;

public class Result extends AppCompatActivity {

    public static TextView edit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);
        edit=(TextView)findViewById(R.id.textView);
        edit.setMovementMethod(new ScrollingMovementMethod());
        Intent sec=getIntent();
        String resp=sec.getStringExtra("resp");
        edit.setText(resp);
    }
}
