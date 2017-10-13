package data.shark.models;

import com.google.gson.JsonObject;

import java.util.Date;

import data.shark.util.UnitConversions;

public class OGUnmanagedObject {

    public String _id;
    public Date createdAt;
    public Date updatedAt;

    public JsonObject toJson() {
        JsonObject result = new JsonObject();
        result.addProperty("_id", this._id);
        result.addProperty("createdAt", UnitConversions.dateToJSONString(this.createdAt));
        result.addProperty("updatedAt", UnitConversions.dateToJSONString(this.updatedAt));
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof OGUnmanagedObject) {
            OGUnmanagedObject other = (OGUnmanagedObject) obj;
            return (this._id != null && this._id.equals(other._id));
        }

        // default: false
        return false;
    }
}
