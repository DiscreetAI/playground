package data.shark.models;

import com.google.gson.JsonElement;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import java.lang.reflect.Type;

public class OGObjectSerializer implements JsonSerializer<OGObject> {

    @Override
    public JsonElement serialize(OGObject src, Type typeOfSrc, JsonSerializationContext context) {
        return src.toJson();
    }

}
