package com.fitbit.authentication;

import data.shark.fitbitcommon.network.BasicHttpRequestBuilder;

/**
 * Created by jboggess on 9/26/16.
 */

public interface RequestSigner {

    void signRequest(BasicHttpRequestBuilder builder);

}
