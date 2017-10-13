package data.shark.models;

import com.google.gson.JsonElement;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import java.lang.reflect.Type;

public class OGUserSerializer implements JsonSerializer<OGUser> {

    @Override
    public JsonElement serialize(OGUser src, Type typeOfSrc, JsonSerializationContext context) {
        return src.toJson();
    }

}
