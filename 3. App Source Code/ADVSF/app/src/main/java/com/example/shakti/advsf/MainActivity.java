package com.example.shakti.advsf;

import android.app.Application;
import android.app.ProgressDialog;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.MediaStore;
import android.text.method.ScrollingMovementMethod;
import android.util.Base64;
import android.util.Log;
import android.util.SparseArray;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.Request;
import com.android.volley.VolleyError;
import com.android.volley.AuthFailureError;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.Random;
import java.io.ByteArrayOutputStream;
import java.util.Hashtable;
import java.util.Map;

import com.google.android.gms.vision.Frame;
import com.google.android.gms.vision.barcode.Barcode;
import com.google.android.gms.vision.barcode.BarcodeDetector;




public class MainActivity extends AppCompatActivity {
    private static int RESULT_LOAD_IMAGE = 1;
    ImageView img;
    TextView txt2;
    TextView edit;
    Random r=new Random();
    static int flag=0;
    BarcodeDetector detector;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        img=(ImageView) findViewById(R.id.imgView);
        edit=(TextView)findViewById(R.id.editText9);
        Button buttonLoadImage = (Button) findViewById(R.id.buttonLoadPicture);
        detector =
                new BarcodeDetector.Builder(getApplicationContext())
                        .setBarcodeFormats(Barcode.QR_CODE)
                        .build();
        buttonLoadImage.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {

                Intent i = new Intent(
                        Intent.ACTION_PICK,
                        android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                startActivityForResult(i, RESULT_LOAD_IMAGE);
            }
        });
        Intent intent = getIntent();
        String action = intent.getAction();
        String type = intent.getType();

        if (Intent.ACTION_SEND.equals(action) && type != null) {
             if (type.startsWith("image/")) {
                handleSendImage(intent); // Handle single image being sent
            }
        }
    }
    void handleSendImage(Intent intent){
        Uri imageUri = (Uri) intent.getParcelableExtra(Intent.EXTRA_STREAM);
        if (imageUri != null) {
            img.setImageURI(imageUri);
        }
    }

    public void scanClicked(View v){
        Bitmap bmp=((BitmapDrawable)img.getDrawable()).getBitmap();
        Frame frame = new Frame.Builder().setBitmap(bmp).build();
        SparseArray<Barcode> barcodes = detector.detect(frame);
        String name1 = Integer.toString(r.nextInt(2000000));
        String pk=edit.getText().toString();
        pk.trim();
        String bar="";
        Barcode thisCode;
        if(edit.getText().length()<10){
            Toast.makeText(MainActivity.this, "Please enter valid Student ID", Toast.LENGTH_SHORT).show();
        }
        else if(barcodes.size()!=0) {
            thisCode = barcodes.valueAt(0);
            bar=thisCode.rawValue;
            Log.d("barc",bar);
            barcode(bar);
        }
        else
            Toast.makeText(MainActivity.this, "No barcode detected", Toast.LENGTH_SHORT).show();

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {
            Uri selectedImage = data.getData();
            String[] filePathColumn = { MediaStore.Images.Media.DATA };

            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            String picturePath = cursor.getString(columnIndex);
            cursor.close();

            ImageView imageView = (ImageView) findViewById(R.id.imgView);
            imageView.setImageBitmap(BitmapFactory.decodeFile(picturePath));
        }
    }

    public String getStringImage(Bitmap bmp){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        int x=bmp.getByteCount();
        int qual=100;
        if(x>500000) {
            qual =80;
        }
        Log.d("sizes",Integer.toString(x));
        bmp.compress(Bitmap.CompressFormat.JPEG, qual, baos);
        Log.d("size2",Integer.toString(bmp.getByteCount()));
        byte[] imageBytes = baos.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;
    }

    private void uploadImage(){
        //Showing the progress dialog
        String UPLOAD_URL="http://eportaltest.tatastrive.com/Decosystem/ADVS/imgver.php";
        final ProgressDialog loading = ProgressDialog.show(this,"Uploading...","Please wait...",false,false);
        StringRequest stringRequest = new StringRequest(Request.Method.POST, UPLOAD_URL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String s) {
                        //Disimissing the progress dialog
                        loading.dismiss();
                        //Showing toast message of the response
                        Log.d("resp",s);
                        Intent myIntent = new Intent(MainActivity.this, Result.class);
                        myIntent.putExtra("resp",s);
                        startActivity(myIntent);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError volleyError) {
                        //Dismissing the progress dialog
                        loading.dismiss();
                        volleyError.printStackTrace();
                        //Showing toast
                        Toast.makeText(MainActivity.this, "Some Error", Toast.LENGTH_LONG).show();
                        //Log.d("err",volleyError.getMessage().toString());
                    }
                }){
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                //Converting Bitmap to String
                String image1 = getStringImage(((BitmapDrawable)img.getDrawable()).getBitmap());

                String name1 = Integer.toString(r.nextInt(2000000));
                String pk=edit.getText().toString();
                pk.trim();
                //Creating parameters
                Map<String,String> params = new Hashtable<String, String>();

                //Adding parameters
                params.put("pk",pk);
                params.put("image",image1);
                params.put("name",name1);
                Log.d("params","sent");
                //returning parameters
                return params;
            }
        };

        //Creating a Request Queue
        RequestQueue requestQueue = Volley.newRequestQueue(this);

        //Adding request to the queue
        stringRequest.setRetryPolicy(new DefaultRetryPolicy(25000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestQueue.add(stringRequest);
    }
    private void barcode(final String bar){
        //Showing the progress dialog
        String UPLOAD_URL="http://eportaltest.tatastrive.com/Decosystem/ADVS/qrver.php";
        final ProgressDialog loading = ProgressDialog.show(this,"Uploading...","Please wait...",false,false);
        StringRequest stringRequest = new StringRequest(Request.Method.POST, UPLOAD_URL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String s) {
                        //Disimissing the progress dialog
                        loading.dismiss();
                        //Showing toast message of the response
                        Log.d("resp",s);
                        Intent myIntent = new Intent(MainActivity.this, Result.class);
                        myIntent.putExtra("resp",s);
                        startActivity(myIntent);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError volleyError) {
                        //Dismissing the progress dialog
                        loading.dismiss();
                        volleyError.printStackTrace();
                        //Showing toast
                        Toast.makeText(MainActivity.this, "Some Error", Toast.LENGTH_LONG).show();
                        //Log.d("err",volleyError.getMessage().toString());
                    }
                }){
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                //Gettting Barcode
                String name1 = Integer.toString(r.nextInt(2000000));
                String pk=edit.getText().toString();
                pk.trim();
                //Creating parameters
                Map<String,String> params = new Hashtable<String, String>();

                //Adding parameters
                params.put("pk",pk);
                params.put("bar",bar);
                params.put("name",name1);
                Log.d("params","sent");
                //returning parameters
                return params;
            }
        };

        //Creating a Request Queue
        RequestQueue requestQueue = Volley.newRequestQueue(this);

        //Adding request to the queue
        stringRequest.setRetryPolicy(new DefaultRetryPolicy(25000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestQueue.add(stringRequest);
    }
    public void verifyClicked(View v){
        if(edit.getText().length()<10){
            Toast.makeText(MainActivity.this, "Please enter valid Student ID", Toast.LENGTH_SHORT).show();
        }
        else{
            uploadImage();
        }
    }
}
