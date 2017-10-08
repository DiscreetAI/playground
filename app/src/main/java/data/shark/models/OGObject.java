package data.shark.models;

import com.google.gson.JsonObject;

import java.util.Date;
import java.util.UUID;

import io.realm.Realm;
import io.realm.RealmModel;
import io.realm.RealmObject;
import data.shark.util.UnitConversions;

public class OGObject extends RealmObject implements data.shark.models.OGManagedObject {

    public String uuid = UUID.randomUUID().toString();
    public String _id;
    public Date createdAt;
    public Date updatedAt;
    public boolean isSynchronized = false;
    // flag to indicate an object is locally deleted, but still needs to stick around for sync
    public boolean isDeleted = false;

    public static data.shark.models.OGManagedObject findObjectWithObjectId(Class type, String objectId) {
        data.shark.models.OGManagedObject result = null;
        if (type != null && objectId != null) {
            Realm realm = Realm.getDefaultInstance();
            RealmModel obj = realm.where(type).equalTo("_id", objectId).findFirst();
            if (obj instanceof data.shark.models.OGManagedObject) {
                result = (data.shark.models.OGManagedObject) obj;
            }
        }
        return result;
    }

    public static OGManagedObject findObjectWithUUID(Class type, String uuid) {
        OGManagedObject result = null;
        if (type != null && uuid != null) {
            Realm realm = Realm.getDefaultInstance();
            RealmModel obj = realm.where(type).equalTo("uuid", uuid).findFirst();
            if (obj instanceof OGManagedObject) {
                result = (OGManagedObject) obj;
            }
        }
        return result;
    }

    @Override
    public String getUUID() {
        return uuid;
    }

    @Override
    public void setUUID(String uuid) {
        this.uuid = uuid;
    }

    @Override
    public String getObjectId() {
        return _id;
    }

    @Override
    public void setObjectId(String objectId) {
        _id = objectId;
    }

    @Override
    public Date getCreatedAt() {
        return createdAt;
    }

    @Override
    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    @Override
    public Date getUpdatedAt() {
        return updatedAt;
    }

    @Override
    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    @Override
    public boolean isSynchronized() {
        return isSynchronized;
    }

    @Override
    public void setSynchronized(boolean aSynchronized) {
        isSynchronized = aSynchronized;
    }

    @Override
    public boolean isDeleted() {
        return isDeleted;
    }

    @Override
    public void setDeleted(boolean deleted) {
        isDeleted = deleted;
    }

    @Override
    public String syncType() {
        return "";
    }

    @Override
    public void fromJson(JsonObject json) {
        if (json.get("_id") != null && json.get("_id").toString() != null) {
            this._id = json.get("_id").toString();
        }
        if (json.get("createdAt") != null && json.get("createdAt").toString() != null) {
            this.createdAt = UnitConversions.dateFromJSONString(json.get("createdAt").toString());
        }
        if (json.get("updatedAt") != null && json.get("updatedAt").toString() != null) {
            this.updatedAt = UnitConversions.dateFromJSONString(json.get("updatedAt").toString());
        }
    }

    public JsonObject toJson() {
        JsonObject result = new JsonObject();
        result.addProperty("_id", this._id);
        result.addProperty("createdAt", UnitConversions.dateToJSONString(this.createdAt));
        result.addProperty("updatedAt", UnitConversions.dateToJSONString(this.updatedAt));
        return result;
    }

    @Override
    public JsonObject toPushJson() {
        return toJson();
    }

    @Override
    public JsonObject toPullJson() {
        return toJson();
    }

    public void markDeleted() {

    }

    public Class<? extends OGManagedObject> classForSyncType(String type) {
        if (type == null) {
            return OGObject.class;
        }

        return OGObject.class;
    }

    @Override
    public void syncUpstream(boolean startSync) {

    }

    @Override
    public OGManagedObject getLocalObject() {
        return null;
    }

    @Override
    public void overwriteWithRemoteCopy(OGManagedObject remoteObj) {

    }

    @Override
    public void deleteObject() {

    }

}
