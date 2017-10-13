package data.shark.models;

import android.util.Log;

import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Set;

import io.realm.Realm;
import io.realm.RealmModel;

public interface OGManagedObject {

    String LOG_TAG = "OGManagedObject";

    /**
     * Returns the managed object with the given UUID, if it exists.
     *
     * @param uuid A unique local UUID.
     * @return The managed object with the given UUID, if it exists. Otherwise,
     * returns null.
     */
    static OGManagedObject findWithUUID(String uuid) {
        final OGManagedObject[] result = new OGManagedObject[1];
        if (uuid == null) {
            return null;
        }

        Realm realm = null;
        try {
            Realm.init(OGApplication.getAppContext());
            realm = Realm.getDefaultInstance();
            realm.executeTransaction(realm1 -> {
                Set<Class<? extends RealmModel>> schemaClasses = realm1.getConfiguration().getRealmObjectClasses();

                for (Class clazz : schemaClasses) {
                    OGManagedObject[] obj = (OGManagedObject[]) realm1.where(clazz).equalTo("uuid", uuid).findAll().toArray();
                    if (obj.length > 0) {
                        result[0] = obj[0];
                        break;
                    }
                }
            });
        } finally {
            if (realm != null) {
                realm.close();
            }
            return result[0];
        }
    }

    /**
     * Returns the managed object with the given (server) ObjectId, if it exists.
     *
     * @param objectId A unique server ID.
     * @return The managed object with the given (server) ObjectId, if it exists.
     */
    static OGManagedObject findWithObjectId(String objectId) {
        final OGManagedObject[] result = new OGManagedObject[1];
        String oid = objectId;
        if (oid == null) {
            return null;
        }

        Realm realm = null;
        try {
            realm = Realm.getDefaultInstance();
            realm.executeTransaction(realm1 -> {
                Set<Class<? extends RealmModel>> schemaClasses = realm1.getConfiguration().getRealmObjectClasses();

                for (Class clazz : schemaClasses) {
                    OGManagedObject[] obj = (OGManagedObject[]) realm1.where(clazz).equalTo("_id", objectId).findAll().toArray();
                    if (obj.length > 0) {
                        result[0] = obj[0];
                        break;
                    }
                }
            });
        } finally {
            if (realm != null) {
                realm.close();
            }
            return result[0];
        }
    }

    /**
     * @return The class of the managed object.
     */
    static Class<? extends OGManagedObject> classForSyncType(String type) {
        switch (type) {
            default:
                return OGObject.class;
        }
    }

    static void syncWithRemoteCopy(OGManagedObject remoteCopy) {
        String oid = remoteCopy.getObjectId();
        if (oid != null) {
            String type = remoteCopy.syncType();
            Log.d(LOG_TAG, "Sync -- " + type + " " + oid);
        }

        // check if local copy exists
        OGManagedObject localCopy = OGManagedObject.findWithObjectId(remoteCopy.getObjectId());
        if (localCopy != null) {
            // TODO: localCopy.syncDownstream(localCopy.getUUID(), remoteCopy);
            // TODO: localCopy.deduplicate();
        } else {
            // just save the remote copy locally -- create case
            remoteCopy.setSynchronized(true);
            // TODO: remoteCopy.createOrUpdate()
            // TODO: remoteCopy.deduplicate();
        }
    }

    static List<OGManagedObject> findUnsyncedObjects(String type, OGUser owner) {
        final List<OGManagedObject> results = new ArrayList<OGManagedObject>();
        if (owner == null) {
            return results;
        }

        Realm realm = null;
        try {
            realm = Realm.getDefaultInstance();
            realm.executeTransaction(realm1 -> {
                Set<Class<? extends RealmModel>> schemaClasses = realm1.getConfiguration().getRealmObjectClasses();

                for (Class clazz : schemaClasses) {
                    OGManagedObject[] objs = (OGManagedObject[]) realm1.where(clazz).equalTo("synchronized", false)
                            .equalTo("deleted", false).equalTo("owner", OGUser.currentUser()._id)
                            .findAll().toArray();
                    if (objs.length > 0) {
                        for (OGManagedObject obj : objs) {
                            results.add(obj);
                        }
                        break;
                    }
                }
            });
        } finally {
            if (realm != null) {
                realm.close();
            }
            return results;
        }
    }

    String getUUID();

    void setUUID(String uuid);

    String getObjectId();

    void setObjectId(String objectId);

    Date getCreatedAt();

    void setCreatedAt(Date createdAt);

    Date getUpdatedAt();

    void setUpdatedAt(Date updatedAt);

    boolean isSynchronized();

    void setSynchronized(boolean isSynchronized);

    boolean isDeleted();

    void setDeleted(boolean isDeleted);

    /**
     * @return Returns the server sync type for this object.
     */
    String syncType();

    /**
     * Set or update values from the given JSON data.
     *
     * @param json JSON representation of the managed object.
     */
    void fromJson(JsonObject json);

    /**
     * @return JSON representation of the managed object.
     */
    JsonObject toJson();

    /**
     * @return JSON representation of the managed object to send to the server during sync (upstream).
     */
    JsonObject toPushJson();

    /**
     * @return JSON representation of the managed object retrieved from the server during sync (downstream).
     */
    JsonObject toPullJson();

    void syncUpstream(boolean startSync);

    OGManagedObject getLocalObject();

    void overwriteWithRemoteCopy(OGManagedObject remoteObj);

    void deleteObject();
}
