package data.shark.models;

import com.google.gson.JsonObject;

import java.util.Date;
import java.util.UUID;

import io.realm.Realm;
import io.realm.RealmObject;
import data.shark.util.Authentication;
import data.shark.util.UnitConversions;

public class OGUser extends RealmObject implements OGManagedObject {

    public String uuid = UUID.randomUUID().toString();
    public String _id;
    public Date createdAt;
    public Date updatedAt;
    public boolean isSynchronized = false;
    // flag to indicate an object is locally deleted, but still needs to stick around for sync
    public boolean isDeleted = false;
    public String email;
    public String firstName;
    public String lastName;
    public String location;
    public String gender;
    public String role;
    public java.util.Date dateOfBirth;
    public boolean emailVerified = false;
    public double bioHeight = 0; // in kg
    public double bioWeight = 0; // in kg
    public String avatarUrl;
    public String avatarOptimizedUrl;
    public String avatarThumbnailUrl;
    public String fitbitAccessToken;
    public String fitbitRefreshToken;
    public boolean isPrivate = false;
    public int statTrackCount = 0;
    public int statFollowerCount = 0;
    public int statFollowingCount = 0;
    public boolean prefNotificationCommunity = true;
    public boolean prefNotificationReminder = true;
    public String mainTrack; // main track ObjectID
    public boolean trackChanged;

    public static OGUser findWithObjectId(String objectId) {
        final OGUser[] result = {null};
        if (objectId != null) {
            Realm realm;
            try {
                Realm.init(OGApplication.getAppContext());
                realm = Realm.getDefaultInstance();
                realm.executeTransaction(realm1 -> result[0] = realm1.where(OGUser.class).equalTo("_id", objectId).findFirst());
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            } finally {
                return result[0];
            }
        }
        return null;
    }

    public static OGUser currentUser() {
        OGUser result = null;
        String currentUserId = Authentication.getInstance().getCurrentUserId();
        if (currentUserId != null) {
            result = findWithObjectId(currentUserId);
        }
        return result;
    }

    public boolean isFitbitLoggedIn() {
        return fitbitAccessToken != null && fitbitRefreshToken != null;
    }

    @Override
    public String getUUID() {
        return uuid;
    }

    @Override
    public void setUUID(String uuid) {
        this.uuid = uuid;
    }

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
    public void setSynchronized(boolean isSynchronized) {
        this.isSynchronized = isSynchronized;
    }

    @Override
    public boolean isDeleted() {
        return isDeleted;
    }

    @Override
    public void setDeleted(boolean isDeleted) {
        this.isDeleted = isDeleted;
    }

    @Override
    public String syncType() {
        return "OGUser";
    }

    @Override
    public void fromJson(JsonObject json) {

    }

    public JsonObject toJson() {
        JsonObject result = new JsonObject();
        result.addProperty("_id", this._id);
        result.addProperty("createdAt", UnitConversions.dateToJSONString(this.createdAt));
        result.addProperty("updatedAt", UnitConversions.dateToJSONString(this.updatedAt));
        result.addProperty("email", this.email);
        result.addProperty("firstName", this.firstName);
        result.addProperty("lastName", this.lastName);
        result.addProperty("location", this.location);
        result.addProperty("gender", this.gender);
        result.addProperty("role", this.role);
        result.addProperty("dateOfBirth", UnitConversions.dateToJSONString(this.dateOfBirth));
        result.addProperty("emailVerified", this.emailVerified);
        result.addProperty("bioHeight", Double.valueOf(this.bioHeight));
        result.addProperty("bioWeight", Double.valueOf(this.bioWeight));
        result.addProperty("avatarUrl", this.avatarUrl);
        result.addProperty("avatarOptimizedUrl", this.avatarOptimizedUrl);
        result.addProperty("avatarThumbnailUrl", this.avatarThumbnailUrl);
        result.addProperty("fitbitAccessToken", this.fitbitAccessToken);
        result.addProperty("fitbitRefreshToken", this.fitbitRefreshToken);
        result.addProperty("isPrivate", this.isPrivate);
        result.addProperty("statTrackCount", this.statTrackCount);
        result.addProperty("statFollowerCount", this.statFollowerCount);
        result.addProperty("statFollowingCount", this.statFollowingCount);
        result.addProperty("prefNotificationCommunity", this.prefNotificationCommunity);
        result.addProperty("prefNotificationReminder", this.prefNotificationReminder);
        result.addProperty("mainTrack", this.mainTrack);
        return result;
    }

    @Override
    public JsonObject toPushJson() {
        return null;
    }

    @Override
    public JsonObject toPullJson() {
        return null;
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
        isDeleted = true;
    }

    public String fullName() {
        String result = "";
        if (this.firstName != null) {
            result += firstName + " ";
        }
        if (this.lastName != null) {
            result += lastName;
        }
        return result;
    }

    @Override
    public String toString() {
        String result = fullName();
        if (this.email != null) {
            result += " (" + this.email + ")";
        }
        return result;
    }


}
