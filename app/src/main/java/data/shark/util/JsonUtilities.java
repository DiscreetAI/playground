package data.shark.util;

import android.util.Log;

import com.google.gson.JsonElement;
import com.google.gson.JsonNull;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

import java.util.Date;

/**
 * Created by mujtaba on 6/9/17.
 */

public class JsonUtilities {

    public static void addProperty(JsonObject json, String property, Object value) {
        if (json == null || property == null) {
            Log.v("JsonUtilities", "Got unexpected null parameter.");
            return;
        }

        JsonElement element = JsonNull.INSTANCE;
        if (value instanceof Date) {
            element = new JsonPrimitive(UnitConversions.dateToJSONString((Date) value));
        } else if (value instanceof Boolean) {
            element = new JsonPrimitive((Boolean) value);
        } else if (value instanceof Number) {
            element = new JsonPrimitive((Number) value);
        } else {
            // convert to string
            element = new JsonPrimitive(value.toString());
        }
        json.add(property, element);
    }

}
