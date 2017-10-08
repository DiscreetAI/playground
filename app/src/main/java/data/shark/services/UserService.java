package data.shark.services;

import java.util.List;

import io.reactivex.Observable;
import data.shark.models.OGUser;
import data.shark.services.ServiceBodies.FollowResponse;
import data.shark.services.ServiceBodies.FriendRequest;
import data.shark.services.ServiceBodies.PasswordHolder;
import data.shark.services.ServiceBodies.UserProfile;
import retrofit2.Response;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

/**
 * Created by panda on 6/28/2017.
 */

public interface UserService {

    @POST("api/users/{id}")
    Observable<OGUser> updateUserProfile(
            @Path("id") String userId,
            @Body UserProfile userProfile
    );

    @GET("api/users/{id}")
    Observable<OGUser> getUser(
            @Path("id") String userId
    );

    @POST("/api/friend-requests/")
    Observable<Object> follow(
            @Body FriendRequest friendRequest
    );

    @POST("api/users/{id}/unfollow")
    Observable<Response<Void>> unfollow(
            @Path("id") String id
    );

    @GET("api/users/follows/{id}")
    Observable<FollowResponse> isFollowing(
            @Path("id") String targetId
    );

    @GET("api/users/following")
    Observable<List<OGUser>> following();

    @GET("api/users/followers")
    Observable<List<OGUser>> followers();

    @GET("api/users/{id}/following")
    Observable<List<OGUser>> idFollowing(
            @Path("id") String userId
    );

    @GET("api/users/{id}/followers")
    Observable<List<OGUser>> idFollowers(
            @Path("id") String userId
    );


    @POST("api/users/resetPassword")
    Observable<OGUser> resetPassword(
            @Body PasswordHolder passwordHolder
    );
//    @GET("api/users/follows/{id}")
//    Observable<List<OGUser>> followsId(
//            @Path("id") String userId
//    );
}
